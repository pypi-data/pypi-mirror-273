from __future__ import annotations

import functools
from typing import TYPE_CHECKING

import pytest
import torch
from scipy.stats import ortho_group

from tests.project.conftest import LATENT_DIM

from latentis.space import LatentSpace
from latentis.transform import Identity, TransformSequence
from latentis.transform.base import Centering
from latentis.transform.projection import (
    RelativeProjection,
    angular_proj,
    change_of_basis_proj,
    cosine_proj,
    euclidean_proj,
    l1_proj,
    lp_proj,
    pointwise_wrapper,
)

if TYPE_CHECKING:
    from latentis.types import Space

from latentis.utils import seed_everything


def random_ortho_matrix(random_seed: int) -> torch.Tensor:
    return torch.as_tensor(ortho_group.rvs(LATENT_DIM, random_state=random_seed), dtype=torch.double)


def random_perm_matrix(random_seed: int) -> torch.Tensor:
    seed_everything(random_seed)
    return torch.as_tensor(torch.randperm(LATENT_DIM), dtype=torch.long)


def random_isotropic_scaling(random_seed: int) -> torch.Tensor:
    seed_everything(random_seed)
    return torch.randint(1, 100, (1,), dtype=torch.double)


@pytest.mark.parametrize(
    "projection_fn,unsqueeze",
    [
        (cosine_proj, True),
        (angular_proj, True),
        (euclidean_proj, True),
        (l1_proj, True),
        (functools.partial(lp_proj, p=10), True),
    ],
)
def test_pointwise_wrapper(projection_fn, unsqueeze: bool, tensor_space_with_ref):
    x, anchors = tensor_space_with_ref

    vectorized = projection_fn(x, anchors=anchors)
    pointwise = pointwise_wrapper(projection_fn, unsqueeze=unsqueeze)(x, anchors)

    assert torch.allclose(vectorized, pointwise)


@pytest.mark.parametrize(
    "projection_fn,invariance,invariant,abs_transforms,rel_transforms",
    [
        (
            angular_proj,
            lambda x: x @ random_ortho_matrix(random_seed=42),
            True,
            [],
            [],
        ),
        (
            angular_proj,
            lambda x: x @ random_ortho_matrix(random_seed=42) + 100,
            False,
            [],
            [],
        ),
        (
            angular_proj,
            lambda x: x @ random_ortho_matrix(random_seed=42) + 100,
            True,
            [Centering()],
            [],
        ),
        (
            cosine_proj,
            lambda x: x @ random_ortho_matrix(random_seed=42),
            True,
            [],
            [],
        ),
        (
            cosine_proj,
            lambda x: (x + 20) @ random_ortho_matrix(42),
            True,
            [Centering()],
            [],
        ),
        (
            cosine_proj,
            lambda x: (x) @ random_ortho_matrix(42) + 20,
            True,
            [Centering()],
            [],
        ),
        (
            cosine_proj,
            lambda x: (x) @ random_ortho_matrix(42) * 100,
            True,
            [],
            [],
        ),
        (
            cosine_proj,
            lambda x: (x) @ random_ortho_matrix(42) + 20,
            False,
            [],
            [],
        ),
        (
            cosine_proj,
            lambda x: x @ random_ortho_matrix(random_seed=42),
            True,
            [],
            [],
        ),
        (
            euclidean_proj,
            lambda x: (x) @ random_ortho_matrix(42) + 100,
            True,
            [],
            [],
        ),
        (
            l1_proj,
            lambda x: (x) @ random_ortho_matrix(42) + 100,
            False,
            [],
            [],
        ),
        (
            l1_proj,
            lambda x: x[:, random_perm_matrix(42)] + 100,
            True,
            [],
            [],
        ),
        (
            l1_proj,
            lambda x: (x + 100)[:, random_perm_matrix(42)],
            True,
            [],
            [],
        ),
        (
            cosine_proj,
            lambda x: (x + 100) * random_isotropic_scaling(42),
            False,
            [],
            [],
        ),
        (
            cosine_proj,
            lambda x: (x + 100) * random_isotropic_scaling(42),
            True,
            [Centering()],
            [],
        ),
        (
            cosine_proj,
            lambda x: (x + 100) * random_isotropic_scaling(42) + 100,
            True,
            [Centering()],
            [],
        ),
        (
            change_of_basis_proj,
            lambda x: (x + 100) * random_isotropic_scaling(42),
            True,
            [Centering()],
            [],
        ),
        (
            change_of_basis_proj,
            lambda x: (x) * random_isotropic_scaling(42),
            True,
            [],
            [],
        ),
        (
            change_of_basis_proj,
            lambda x: (x) * random_isotropic_scaling(42) + 53,
            False,
            [],
            [],
        ),
    ],
)
def test_invariances(
    projection_fn, x: Space, x_anchors, invariance, invariant, abs_transforms: list, rel_transforms: list
):
    y = invariance(x) if isinstance(x, torch.Tensor) else x.transform(invariance)
    y_anchors = invariance(x_anchors if isinstance(x_anchors, torch.Tensor) else x_anchors.vectors)

    if isinstance(x, LatentSpace):
        y = LatentSpace.like(x, vector_source=y)

    if isinstance(x_anchors, LatentSpace):
        x_anchors = x_anchors.vectors

    abs_transforms = TransformSequence(abs_transforms) if abs_transforms else Identity()
    rel_transforms = TransformSequence(rel_transforms) if rel_transforms else Identity()

    pipeline = RelativeProjection(
        projection_fn=projection_fn,
        abs_transform=abs_transforms,
        rel_transform=rel_transforms,
    )
    pipeline.fit(x_anchors.vectors if isinstance(x_anchors, LatentSpace) else x_anchors)
    x_projected, _ = pipeline.transform(x if isinstance(x, torch.Tensor) else x.vectors)

    pipeline.fit(y_anchors.vectors if isinstance(y_anchors, LatentSpace) else y_anchors)
    y_projected, _ = pipeline.transform(y if isinstance(y, torch.Tensor) else y.vectors)

    assert not invariant or torch.allclose(x_projected, y_projected)

    if isinstance(x, LatentSpace):
        pytest.skip("LatentSpace does not support relative projections.")
        # space_relative = x.to_relative(projection=projection, anchors=x_anchors)
        # assert torch.allclose(space_relative.vectors, x_projected)
