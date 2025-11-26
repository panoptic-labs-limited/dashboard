from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.widget_render_request_input_values import WidgetRenderRequestInputValues


T = TypeVar("T", bound="WidgetRenderRequest")


@_attrs_define
class WidgetRenderRequest:
    """Request to render a single widget.

    Attributes:
        input_values (WidgetRenderRequestInputValues | Unset):
    """

    input_values: WidgetRenderRequestInputValues | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_values: dict[str, Any] | Unset = UNSET
        if not isinstance(self.input_values, Unset):
            input_values = self.input_values.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if input_values is not UNSET:
            field_dict["input_values"] = input_values

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.widget_render_request_input_values import WidgetRenderRequestInputValues

        d = dict(src_dict)
        _input_values = d.pop("input_values", UNSET)
        input_values: WidgetRenderRequestInputValues | Unset
        if isinstance(_input_values, Unset):
            input_values = UNSET
        else:
            input_values = WidgetRenderRequestInputValues.from_dict(_input_values)

        widget_render_request = cls(
            input_values=input_values,
        )

        widget_render_request.additional_properties = d
        return widget_render_request

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
