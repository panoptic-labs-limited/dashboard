from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.layout_type import LayoutType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tab_schema import TabSchema

T = TypeVar("T", bound="TabsSchema")


@_attrs_define
class TabsSchema:
    """Tabs container holding multiple Tab components.

    Attributes:
        id (str): Unique ID for this containers node
        type_ (LayoutType | Unset): Types of containers components.
        default_tab (None | str | Unset): ID of default active tab
        children (list[TabSchema] | Unset):
    """

    id: str
    type_: LayoutType | Unset = UNSET
    default_tab: None | str | Unset = UNSET
    children: list[TabSchema] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        default_tab: None | str | Unset
        if isinstance(self.default_tab, Unset):
            default_tab = UNSET
        else:
            default_tab = self.default_tab

        children: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.children, Unset):
            children = []
            for children_item_data in self.children:
                children_item = children_item_data.to_dict()
                children.append(children_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if default_tab is not UNSET:
            field_dict["default_tab"] = default_tab
        if children is not UNSET:
            field_dict["children"] = children

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tab_schema import TabSchema

        d = dict(src_dict)
        id = d.pop("id")

        _type_ = d.pop("type", UNSET)
        type_: LayoutType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = LayoutType(_type_)

        def _parse_default_tab(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        default_tab = _parse_default_tab(d.pop("default_tab", UNSET))

        _children = d.pop("children", UNSET)
        children: list[TabSchema] | Unset = UNSET
        if _children is not UNSET:
            children = []
            for children_item_data in _children:
                children_item = TabSchema.from_dict(children_item_data)

                children.append(children_item)

        tabs_schema = cls(
            id=id,
            type_=type_,
            default_tab=default_tab,
            children=children,
        )

        tabs_schema.additional_properties = d
        return tabs_schema

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
