from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.layout_type import LayoutType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.column_schema import ColumnSchema
    from ..models.row_schema import RowSchema
    from ..models.widget_schema import WidgetSchema

T = TypeVar("T", bound="TabSchema")


@_attrs_define
class TabSchema:
    """Individual tab within a Tabs container.

    Attributes:
        id (str): Unique ID for this containers node
        title (str):
        type_ (LayoutType | Unset): Types of containers components.
        icon (None | str | Unset):
        disabled (bool | Unset):  Default: False.
        children (list[ColumnSchema | RowSchema | WidgetSchema] | Unset):
    """

    id: str
    title: str
    type_: LayoutType | Unset = UNSET
    icon: None | str | Unset = UNSET
    disabled: bool | Unset = False
    children: list[ColumnSchema | RowSchema | WidgetSchema] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.column_schema import ColumnSchema
        from ..models.row_schema import RowSchema

        id = self.id

        title = self.title

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        icon: None | str | Unset
        if isinstance(self.icon, Unset):
            icon = UNSET
        else:
            icon = self.icon

        disabled = self.disabled

        children: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.children, Unset):
            children = []
            for children_item_data in self.children:
                children_item: dict[str, Any]
                if isinstance(children_item_data, RowSchema):
                    children_item = children_item_data.to_dict()
                elif isinstance(children_item_data, ColumnSchema):
                    children_item = children_item_data.to_dict()
                else:
                    children_item = children_item_data.to_dict()

                children.append(children_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if icon is not UNSET:
            field_dict["icon"] = icon
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if children is not UNSET:
            field_dict["children"] = children

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.column_schema import ColumnSchema
        from ..models.row_schema import RowSchema
        from ..models.widget_schema import WidgetSchema

        d = dict(src_dict)
        id = d.pop("id")

        title = d.pop("title")

        _type_ = d.pop("type", UNSET)
        type_: LayoutType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = LayoutType(_type_)

        def _parse_icon(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        icon = _parse_icon(d.pop("icon", UNSET))

        disabled = d.pop("disabled", UNSET)

        _children = d.pop("children", UNSET)
        children: list[ColumnSchema | RowSchema | WidgetSchema] | Unset = UNSET
        if _children is not UNSET:
            children = []
            for children_item_data in _children:

                def _parse_children_item(data: object) -> ColumnSchema | RowSchema | WidgetSchema:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        children_item_type_0 = RowSchema.from_dict(data)

                        return children_item_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        children_item_type_1 = ColumnSchema.from_dict(data)

                        return children_item_type_1
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    children_item_type_2 = WidgetSchema.from_dict(data)

                    return children_item_type_2

                children_item = _parse_children_item(children_item_data)

                children.append(children_item)

        tab_schema = cls(
            id=id,
            title=title,
            type_=type_,
            icon=icon,
            disabled=disabled,
            children=children,
        )

        tab_schema.additional_properties = d
        return tab_schema

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
