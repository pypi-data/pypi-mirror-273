from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Mapping, Optional, Sequence, Union

import torch
from torch import nn

from latentis.serialize.io_utils import IndexableMixin
from latentis.transform.functional import InverseFn, State, StateFn, TransformFn
from latentis.types import Properties

if TYPE_CHECKING:
    from latentis.types import Space


class Transform(nn.Module, IndexableMixin):
    _STATE_PREFIX: str = "latentis_state_"

    @property
    def properties(self) -> Properties:
        return {
            "name": self.name,
            # "invertible": self.invertible,
        }

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        invertible: bool = False,
    ) -> None:
        super().__init__()
        self._name: Optional[str] = name
        self._invertible: bool = invertible

    @abstractmethod
    def fit_stats():
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self._name

    def _register_state(self, state: State) -> None:
        for key, value in state.items():
            self.register_buffer(f"{Transform._STATE_PREFIX}{key}", value)

    def get_state(self, *keys: str) -> Union[torch.Tensor, Mapping[str, torch.Tensor]]:
        if len(keys) == 1:
            return getattr(self, f"{Transform._STATE_PREFIX}{keys[0]}")

        if len(keys) > 1:
            return {k: getattr(self, f"{Transform._STATE_PREFIX}{k}") for k in keys}

        return {
            k[len(Transform._STATE_PREFIX) :]: v
            for k, v in self.state_dict().items()
            if k.startswith(Transform._STATE_PREFIX)
        }

    def fit(self, x: torch.Tensor, y: torch.Tensor = None) -> "Transform":
        return self

    def transform(self, x: torch.Tensor, y: torch.Tensor = None) -> torch.Tensor:
        raise NotImplementedError

    def fit_transform(self, x: torch.Tensor, y: torch.Tensor = None) -> torch.Tensor:
        return self.fit(x=x, y=y).transform(x=x, y=y)

    def forward(self, x: torch.Tensor, y=None, inverse: bool = False) -> torch.Tensor:
        x, y = self.transform(x=x, y=y) if not inverse else self.inverse_transform(x=x, y=y)

        return {
            "x": x,
            "y": y,
        }

    @property
    def invertible(self) -> bool:
        return self._invertible

    def inverse_transform(self, x: torch.Tensor, y=None) -> torch.Tensor:
        raise RuntimeError(f"Inverse transform not implemented for {type(self).__name__}.")


class SimpleTransform(Transform):
    def __init__(
        self,
        transform_fn: TransformFn,
        state_fn: Optional[StateFn] = None,
        inverse_fn: Optional[InverseFn] = None,
        transform_params: Optional[Mapping[str, Any]] = None,
        state_params: Optional[Mapping[str, Any]] = None,
        inverse_params: Optional[Mapping[str, Any]] = None,
        name: Optional[str] = None,
    ) -> None:
        # TODO: automatically retrieve the reverse_fn from the transform_fn
        super().__init__(name=name)

        self._transform_fn: TransformFn = transform_fn
        self._inverse_fn: Optional[InverseFn] = inverse_fn
        self._state_fn: Optional[State] = state_fn

        self._transform_params: Mapping[str, Any] = {} if transform_params is None else transform_params
        self._state_params: Mapping[str, Any] = {} if state_params is None else state_params
        self._inverse_params: Mapping[str, Any] = {} if inverse_params is None else inverse_params

        self._fitted: bool = False

    @property
    def name(self) -> str:
        return (
            self._name
            if self._name is not None
            else f"{self._transform_fn.__name__}"
            if hasattr(self._transform_fn, "__name__")
            else "transform"
        )

    @property
    def invertible(self) -> bool:
        return self._inverse_fn is not None

    def __repr__(self):
        return f"name={self.name}, reverse_fn={self.inverse_fn.__name__ if self.inverse_fn is not None else None})"

    @property
    def inverse_fn(self) -> Optional[InverseFn]:
        return self._inverse_fn

    def fit(self, x: torch.Tensor, y=None) -> "Transform":
        if self._state_fn is not None:
            self._register_state(self._state_fn(x=x, **self._state_params))

        self._fitted = True
        return self

    def transform(self, x: torch.Tensor, y=None) -> torch.Tensor:
        if not self._fitted and self._state_fn is not None:
            raise RuntimeError("Transform not fitted.")

        return self._transform_fn(x=x, **self._transform_params, **self.get_state()), y

    def inverse_transform(self, x: torch.Tensor, y=None) -> torch.Tensor:
        if not self._fitted and self._state_fn is not None:
            raise RuntimeError("Transform not fitted.")

        # return x, self._inverse_fn(x=y, **self._inverse_params, **self.get_state())
        return self._inverse_fn(x=x, **self._inverse_params, **self.get_state()), y


class Identity(SimpleTransform):
    def __init__(self):
        super().__init__(
            transform_fn=lambda x: x,
            inverse_fn=lambda x: x,
            name="identity",
        )


class TransformSequence(Transform):
    def __init__(self, transforms: Sequence[Transform]):
        super().__init__()
        self.transforms = transforms

    def fit(self, x: Space, y=None) -> "TransformSequence":
        for transform in self.transforms:
            x, y = transform.fit_transform(x=x, y=y)

        return self

    def transform(self, x: Space, y=None) -> torch.Tensor:
        for transform in self.transforms:
            x, y = transform.transform(x=x, y=y)

        return x, y

    @property
    def invertible(self) -> bool:
        return all(transform.invertible for transform in self.transforms)

    def inverse_transform(self, x: Space, y=None) -> torch.Tensor:
        assert self.invertible, "Not all transforms in the sequence are invertible."
        for transform in reversed(self.transforms):
            x, y = transform.inverse_transform(x=x, y=y)

        return x, y


class Estimator(Transform):
    def __init__(
        self,
        *,
        name: Optional[str] = None,
        invertible: bool = False,
        x_space: Optional[torch.Tensor] = None,
        y_space: Optional[torch.Tensor] = None,
    ) -> None:
        super().__init__(name=name, invertible=invertible)

        self._x_space = x_space
        self._y_space = y_space

    def set_spaces(self, x_space: torch.Tensor, y_space: torch.Tensor) -> "Estimator":
        # TODO: decide if we want to keep the shuffling or trust the users
        self._x_space = x_space[torch.randperm(x_space.shape[0])]
        self._y_space = y_space
        return self
