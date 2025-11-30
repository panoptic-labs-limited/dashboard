from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.layout_type import LayoutType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.page_schema import PageSchema

T = TypeVar("T", bound="DashboardStructure")


@_attrs_define
class DashboardStructure:
    """Complete dashboard structure.

    Attributes:
        id (str): Unique ID for dashboard
        title (str):
        type_ (LayoutType | Unset): Types of layout components.
        description (None | str | Unset):
        version (str | Unset):  Default: '1.0.0'.
        children (list[PageSchema] | Unset):
    """

    id: str
    title: str
    type_: LayoutType | Unset = UNSET
    description: None | str | Unset = UNSET
    version: str | Unset = "1.0.0"
    children: list[PageSchema] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title = self.title

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        version = self.version

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
                "title": title,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if description is not UNSET:
            field_dict["description"] = description
        if version is not UNSET:
            field_dict["version"] = version
        if children is not UNSET:
            field_dict["children"] = children

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.page_schema import PageSchema

        d = dict(src_dict)
        id = d.pop("id")

        title = d.pop("title")

        _type_ = d.pop("type", UNSET)
        type_: LayoutType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = LayoutType(_type_)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        version = d.pop("version", UNSET)

        _children = d.pop("children", UNSET)
        children: list[PageSchema] | Unset = UNSET
        if _children is not UNSET:
            children = []
            for children_item_data in _children:
                children_item = PageSchema.from_dict(children_item_data)

                children.append(children_item)

        dashboard_structure = cls(
            id=id,
            title=title,
            type_=type_,
            description=description,
            version=version,
            children=children,
        )

        dashboard_structure.additional_properties = d
        return dashboard_structure

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
