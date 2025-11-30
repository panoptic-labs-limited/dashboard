from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.parameter_binding import ParameterBinding

T = TypeVar("T", bound="WidgetSchemaParams")


@_attrs_define
class WidgetSchemaParams:
    """ """

    additional_properties: dict[str, Any | ParameterBinding] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.parameter_binding import ParameterBinding

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, ParameterBinding):
                field_dict[prop_name] = prop.to_dict()
            else:
                field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.parameter_binding import ParameterBinding

        d = dict(src_dict)
        widget_schema_params = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(data: object) -> Any | ParameterBinding:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_1 = ParameterBinding.from_dict(data)

                    return additional_property_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                return cast(Any | ParameterBinding, data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        widget_schema_params.additional_properties = additional_properties
        return widget_schema_params

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any | ParameterBinding:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any | ParameterBinding) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
