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
    """
    Attributes:
        alias (str): Unique alias for the function
        code (str): Python function code as string
        id (int):
        owner_id (int):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        description (None | str | Unset):
        memory_limit_mb (int | Unset):  Default: 200.
        timeout_seconds (int | Unset):  Default: 30.
    """

    alias: str
    code: str
    id: int
    owner_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    description: None | str | Unset = UNSET
    memory_limit_mb: int | Unset = 200
    timeout_seconds: int | Unset = 30
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        alias = self.alias

        code = self.code

        id = self.id

        owner_id = self.owner_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

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
                "id": id,
                "owner_id": owner_id,
                "created_at": created_at,
                "updated_at": updated_at,
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

        id = d.pop("id")

        owner_id = d.pop("owner_id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        memory_limit_mb = d.pop("memory_limit_mb", UNSET)

        timeout_seconds = d.pop("timeout_seconds", UNSET)

        function_response = cls(
            alias=alias,
            code=code,
            id=id,
            owner_id=owner_id,
            created_at=created_at,
            updated_at=updated_at,
            description=description,
            memory_limit_mb=memory_limit_mb,
            timeout_seconds=timeout_seconds,
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
