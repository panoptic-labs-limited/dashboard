from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.layout_type import LayoutType
from ..models.widget_type import WidgetType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.widget_schema_config import WidgetSchemaConfig
    from ..models.widget_schema_params import WidgetSchemaParams

T = TypeVar("T", bound="WidgetSchema")


@_attrs_define
class WidgetSchema:
    """Widget containing a component instance.

    Attributes:
        id (str): Unique ID for this layout node
        widget_type (WidgetType): Types of widgets available.
        type_ (LayoutType | Unset): Types of layout components.
        component_alias (None | str | Unset):
        params (WidgetSchemaParams | Unset):
        title (None | str | Unset):
        description (None | str | Unset):
        config (WidgetSchemaConfig | Unset):
    """

    id: str
    widget_type: WidgetType
    type_: LayoutType | Unset = UNSET
    component_alias: None | str | Unset = UNSET
    params: WidgetSchemaParams | Unset = UNSET
    title: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    config: WidgetSchemaConfig | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        widget_type = self.widget_type.value

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        component_alias: None | str | Unset
        if isinstance(self.component_alias, Unset):
            component_alias = UNSET
        else:
            component_alias = self.component_alias

        params: dict[str, Any] | Unset = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "widget_type": widget_type,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if component_alias is not UNSET:
            field_dict["component_alias"] = component_alias
        if params is not UNSET:
            field_dict["params"] = params
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if config is not UNSET:
            field_dict["config"] = config

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.widget_schema_config import WidgetSchemaConfig
        from ..models.widget_schema_params import WidgetSchemaParams

        d = dict(src_dict)
        id = d.pop("id")

        widget_type = WidgetType(d.pop("widget_type"))

        _type_ = d.pop("type", UNSET)
        type_: LayoutType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = LayoutType(_type_)

        def _parse_component_alias(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        component_alias = _parse_component_alias(d.pop("component_alias", UNSET))

        _params = d.pop("params", UNSET)
        params: WidgetSchemaParams | Unset
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = WidgetSchemaParams.from_dict(_params)

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _config = d.pop("config", UNSET)
        config: WidgetSchemaConfig | Unset
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = WidgetSchemaConfig.from_dict(_config)

        widget_schema = cls(
            id=id,
            widget_type=widget_type,
            type_=type_,
            component_alias=component_alias,
            params=params,
            title=title,
            description=description,
            config=config,
        )

        widget_schema.additional_properties = d
        return widget_schema

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
