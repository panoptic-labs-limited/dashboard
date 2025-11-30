from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.column_width import ColumnWidth
from ..models.layout_type import LayoutType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.row_schema import RowSchema
    from ..models.widget_schema import WidgetSchema

T = TypeVar("T", bound="ColumnSchema")


@_attrs_define
class ColumnSchema:
    """Column layout container.

    Attributes:
        id (str): Unique ID for this layout node
        type_ (LayoutType | Unset): Types of layout components.
        width (ColumnWidth | Unset): Standard column widths.
        gap (None | str | Unset): Gap between children (CSS)
        children (list[ColumnSchema | RowSchema | WidgetSchema] | Unset):
    """

    id: str
    type_: LayoutType | Unset = UNSET
    width: ColumnWidth | Unset = UNSET
    gap: None | str | Unset = UNSET
    children: list[ColumnSchema | RowSchema | WidgetSchema] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.row_schema import RowSchema

        id = self.id

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        width: str | Unset = UNSET
        if not isinstance(self.width, Unset):
            width = self.width.value

        gap: None | str | Unset
        if isinstance(self.gap, Unset):
            gap = UNSET
        else:
            gap = self.gap

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
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if width is not UNSET:
            field_dict["width"] = width
        if gap is not UNSET:
            field_dict["gap"] = gap
        if children is not UNSET:
            field_dict["children"] = children

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.row_schema import RowSchema
        from ..models.widget_schema import WidgetSchema

        d = dict(src_dict)
        id = d.pop("id")

        _type_ = d.pop("type", UNSET)
        type_: LayoutType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = LayoutType(_type_)

        _width = d.pop("width", UNSET)
        width: ColumnWidth | Unset
        if isinstance(_width, Unset):
            width = UNSET
        else:
            width = ColumnWidth(_width)

        def _parse_gap(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        gap = _parse_gap(d.pop("gap", UNSET))

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

        column_schema = cls(
            id=id,
            type_=type_,
            width=width,
            gap=gap,
            children=children,
        )

        column_schema.additional_properties = d
        return column_schema

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
