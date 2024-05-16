from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

import pytest
import torch
from torch import Tensor

from latentis.space import LatentSpace
from latentis.utils import seed_everything

if TYPE_CHECKING:
    from latentis.types import Space


class Space1Params(object):
    seed_everything(42)
    instances = [
        LatentSpace(
            vector_source=torch.randn(1000, 128, dtype=torch.double),
        ),
        torch.randn(1000, 128, dtype=torch.double),
    ]


@pytest.fixture(params=Space1Params().instances, scope="session")
def space1(request) -> Space:
    return request.param


class Space2Params(object):
    seed_everything(42)
    instances = [
        LatentSpace(
            vector_source=torch.randn(53, 250, dtype=torch.double),
        ),
        torch.randn(53, 250, dtype=torch.double),
    ]


@pytest.fixture(params=Space2Params().instances, scope="session")
def space2(request) -> Space:
    return request.param


class ParallelSpaces(object):
    instances = [
        (
            LatentSpace(
                vector_source=torch.randn(space1_n, space_1_dim, dtype=torch.double),
            ),
            LatentSpace(
                vector_source=torch.randn(space2_n, space2_dim, dtype=torch.double),
            ),
        )
        for (space1_n, space_1_dim), (space2_n, space2_dim) in [
            ((50, 250), (50, 250)),
            ((50, 250), (50, 300)),
            ((50, 300), (50, 250)),
            ((1000, 100), (1000, 500)),
            ((1000, 500), (1000, 100)),
        ]
    ] + [
        (
            torch.randn(space1_n, space_1_dim, dtype=torch.double),
            torch.randn(space2_n, space2_dim, dtype=torch.double),
        )
        for (space1_n, space_1_dim), (space2_n, space2_dim) in [
            ((50, 250), (50, 250)),
            ((50, 250), (50, 300)),
            ((50, 300), (50, 250)),
            ((1000, 100), (1000, 500)),
            ((1000, 500), (1000, 100)),
        ]
    ]


@pytest.fixture(params=ParallelSpaces().instances)
def parallel_spaces(request) -> Tuple[Space, Space]:
    return request.param


class TensorSpaceWithRef(object):
    seed_everything(42)
    instances = [
        (
            torch.randn(space1_n, space1_dim, dtype=torch.double),
            torch.randn(space2_n, space2_dim, dtype=torch.double),
        )
        for (space1_n, space1_dim), (space2_n, space2_dim) in [
            ((10, 250), (100, 250)),
            ((300, 300), (20, 300)),
            ((100, 700), (42, 700)),
        ]
    ]


@pytest.fixture(params=TensorSpaceWithRef().instances)
def tensor_space_with_ref(request) -> Tuple[Tensor, Tensor]:
    return request.param
