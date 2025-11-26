from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="FunctionResponse")


@_attrs_define
class FunctionResponse:
    """Schema for function response.

    Attributes:
        id (int):
        alias (str):
        code (str):
        owner_id (int):
        memory_limit_mb (int):
        timeout_seconds (int):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        description (None | str | Unset):
    """

    id: int
    alias: str
    code: str
    owner_id: int
    memory_limit_mb: int
    timeout_seconds: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    description: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        alias = self.alias

        code = self.code

        owner_id = self.owner_id

        memory_limit_mb = self.memory_limit_mb

        timeout_seconds = self.timeout_seconds

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "alias": alias,
                "code": code,
                "owner_id": owner_id,
                "memory_limit_mb": memory_limit_mb,
                "timeout_seconds": timeout_seconds,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        alias = d.pop("alias")

        code = d.pop("code")

        owner_id = d.pop("owner_id")

        memory_limit_mb = d.pop("memory_limit_mb")

        timeout_seconds = d.pop("timeout_seconds")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        function_response = cls(
            id=id,
            alias=alias,
            code=code,
            owner_id=owner_id,
            memory_limit_mb=memory_limit_mb,
            timeout_seconds=timeout_seconds,
            created_at=created_at,
            updated_at=updated_at,
            description=description,
        )

        function_response.additional_properties = d
        return function_response

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
