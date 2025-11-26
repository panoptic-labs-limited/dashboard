from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FunctionCreate")


@_attrs_define
class FunctionCreate:
    """
    Attributes:
        alias (str): Unique alias for the function
        code (str): Python function code as string
        description (None | str | Unset):
        memory_limit_mb (int | Unset):  Default: 200.
        timeout_seconds (int | Unset):  Default: 30.
    """

    alias: str
    code: str
    description: None | str | Unset = UNSET
    memory_limit_mb: int | Unset = 200
    timeout_seconds: int | Unset = 30
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        alias = self.alias

        code = self.code

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        memory_limit_mb = self.memory_limit_mb

        timeout_seconds = self.timeout_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "alias": alias,
                "code": code,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if memory_limit_mb is not UNSET:
            field_dict["memory_limit_mb"] = memory_limit_mb
        if timeout_seconds is not UNSET:
            field_dict["timeout_seconds"] = timeout_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        alias = d.pop("alias")

        code = d.pop("code")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        memory_limit_mb = d.pop("memory_limit_mb", UNSET)

        timeout_seconds = d.pop("timeout_seconds", UNSET)

        function_create = cls(
            alias=alias,
            code=code,
            description=description,
            memory_limit_mb=memory_limit_mb,
            timeout_seconds=timeout_seconds,
        )

        function_create.additional_properties = d
        return function_create

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
