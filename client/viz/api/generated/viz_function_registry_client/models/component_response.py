from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.component_metadata import ComponentMetadata
    from ..models.component_parameter import ComponentParameter

T = TypeVar("T", bound="ComponentResponse")


@_attrs_define
class ComponentResponse:
    """Schema for component response.

    Attributes:
        id (int):
        alias (str):
        class_name (str):
        source_code (str):
        parameters (list[ComponentParameter]):
        owner_id (int):
        memory_limit_mb (int):
        timeout_seconds (int):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        description (None | str | Unset):
        metadata (ComponentMetadata | None | Unset):
    """

    id: int
    alias: str
    class_name: str
    source_code: str
    parameters: list[ComponentParameter]
    owner_id: int
    memory_limit_mb: int
    timeout_seconds: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    description: None | str | Unset = UNSET
    metadata: ComponentMetadata | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.component_metadata import ComponentMetadata

        id = self.id

        alias = self.alias

        class_name = self.class_name

        source_code = self.source_code

        parameters = []
        for parameters_item_data in self.parameters:
            parameters_item = parameters_item_data.to_dict()
            parameters.append(parameters_item)

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

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, ComponentMetadata):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "alias": alias,
                "class_name": class_name,
                "source_code": source_code,
                "parameters": parameters,
                "owner_id": owner_id,
                "memory_limit_mb": memory_limit_mb,
                "timeout_seconds": timeout_seconds,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.component_metadata import ComponentMetadata
        from ..models.component_parameter import ComponentParameter

        d = dict(src_dict)
        id = d.pop("id")

        alias = d.pop("alias")

        class_name = d.pop("class_name")

        source_code = d.pop("source_code")

        parameters = []
        _parameters = d.pop("parameters")
        for parameters_item_data in _parameters:
            parameters_item = ComponentParameter.from_dict(parameters_item_data)

            parameters.append(parameters_item)

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

        def _parse_metadata(data: object) -> ComponentMetadata | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = ComponentMetadata.from_dict(data)

                return metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ComponentMetadata | None | Unset, data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        component_response = cls(
            id=id,
            alias=alias,
            class_name=class_name,
            source_code=source_code,
            parameters=parameters,
            owner_id=owner_id,
            memory_limit_mb=memory_limit_mb,
            timeout_seconds=timeout_seconds,
            created_at=created_at,
            updated_at=updated_at,
            description=description,
            metadata=metadata,
        )

        component_response.additional_properties = d
        return component_response

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
