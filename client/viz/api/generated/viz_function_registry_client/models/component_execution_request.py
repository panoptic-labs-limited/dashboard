from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.execution_stage import ExecutionStage
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.component_execution_request_params import ComponentExecutionRequestParams


T = TypeVar("T", bound="ComponentExecutionRequest")


@_attrs_define
class ComponentExecutionRequest:
    """Request to execute a component.

    Attributes:
        stage (ExecutionStage | Unset): Execution stages for components.
        params (ComponentExecutionRequestParams | Unset):
    """

    stage: ExecutionStage | Unset = UNSET
    params: ComponentExecutionRequestParams | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        stage: str | Unset = UNSET
        if not isinstance(self.stage, Unset):
            stage = self.stage.value

        params: dict[str, Any] | Unset = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if stage is not UNSET:
            field_dict["stage"] = stage
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.component_execution_request_params import ComponentExecutionRequestParams

        d = dict(src_dict)
        _stage = d.pop("stage", UNSET)
        stage: ExecutionStage | Unset
        if isinstance(_stage, Unset):
            stage = UNSET
        else:
            stage = ExecutionStage(_stage)

        _params = d.pop("params", UNSET)
        params: ComponentExecutionRequestParams | Unset
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = ComponentExecutionRequestParams.from_dict(_params)

        component_execution_request = cls(
            stage=stage,
            params=params,
        )

        component_execution_request.additional_properties = d
        return component_execution_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
