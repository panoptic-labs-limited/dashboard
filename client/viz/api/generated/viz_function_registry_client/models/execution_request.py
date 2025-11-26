from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.execution_request_params import ExecutionRequestParams


T = TypeVar("T", bound="ExecutionRequest")


@_attrs_define
class ExecutionRequest:
    """Request to execute a function.

    Attributes:
        params (ExecutionRequestParams | Unset):
    """

    params: ExecutionRequestParams | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        params: dict[str, Any] | Unset = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.execution_request_params import ExecutionRequestParams

        d = dict(src_dict)
        _params = d.pop("params", UNSET)
        params: ExecutionRequestParams | Unset
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = ExecutionRequestParams.from_dict(_params)

        execution_request = cls(
            params=params,
        )

        execution_request.additional_properties = d
        return execution_request

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
