from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.component_metadata import ComponentMetadata
    from ..models.component_parameter import ComponentParameter

T = TypeVar("T", bound="ComponentCreate")


@_attrs_define
class ComponentCreate:
    """Schema for creating a new component.

    Attributes:
        alias (str): Unique identifier for the component
        class_name (str): Name of the component class
        source_code (str): Complete Python source code
        description (None | str | Unset):
        parameters (list[ComponentParameter] | Unset):
        metadata (ComponentMetadata | None | Unset):
        memory_limit_mb (int | Unset):  Default: 200.
        timeout_seconds (int | Unset):  Default: 30.
    """

    alias: str
    class_name: str
    source_code: str
    description: None | str | Unset = UNSET
    parameters: list[ComponentParameter] | Unset = UNSET
    metadata: ComponentMetadata | None | Unset = UNSET
    memory_limit_mb: int | Unset = 200
    timeout_seconds: int | Unset = 30
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.component_metadata import ComponentMetadata

        alias = self.alias

        class_name = self.class_name

        source_code = self.source_code

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        parameters: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = []
            for parameters_item_data in self.parameters:
                parameters_item = parameters_item_data.to_dict()
                parameters.append(parameters_item)

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, ComponentMetadata):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        memory_limit_mb = self.memory_limit_mb

        timeout_seconds = self.timeout_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "alias": alias,
                "class_name": class_name,
                "source_code": source_code,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if memory_limit_mb is not UNSET:
            field_dict["memory_limit_mb"] = memory_limit_mb
        if timeout_seconds is not UNSET:
            field_dict["timeout_seconds"] = timeout_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.component_metadata import ComponentMetadata
        from ..models.component_parameter import ComponentParameter

        d = dict(src_dict)
        alias = d.pop("alias")

        class_name = d.pop("class_name")

        source_code = d.pop("source_code")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _parameters = d.pop("parameters", UNSET)
        parameters: list[ComponentParameter] | Unset = UNSET
        if _parameters is not UNSET:
            parameters = []
            for parameters_item_data in _parameters:
                parameters_item = ComponentParameter.from_dict(parameters_item_data)

                parameters.append(parameters_item)

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

        memory_limit_mb = d.pop("memory_limit_mb", UNSET)

        timeout_seconds = d.pop("timeout_seconds", UNSET)

        component_create = cls(
            alias=alias,
            class_name=class_name,
            source_code=source_code,
            description=description,
            parameters=parameters,
            metadata=metadata,
            memory_limit_mb=memory_limit_mb,
            timeout_seconds=timeout_seconds,
        )

        component_create.additional_properties = d
        return component_create

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
