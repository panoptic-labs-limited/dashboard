from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.dashboard_render_response_input_values import DashboardRenderResponseInputValues
    from ..models.widget_render_result import WidgetRenderResult


T = TypeVar("T", bound="DashboardRenderResponse")


@_attrs_define
class DashboardRenderResponse:
    """Response from rendering a dashboard.

    Attributes:
        dashboard_id (str):
        input_values (DashboardRenderResponseInputValues):
        widgets (list[WidgetRenderResult]):
        total_execution_time_ms (float):
    """

    dashboard_id: str
    input_values: DashboardRenderResponseInputValues
    widgets: list[WidgetRenderResult]
    total_execution_time_ms: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dashboard_id = self.dashboard_id

        input_values = self.input_values.to_dict()

        widgets = []
        for widgets_item_data in self.widgets:
            widgets_item = widgets_item_data.to_dict()
            widgets.append(widgets_item)

        total_execution_time_ms = self.total_execution_time_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dashboard_id": dashboard_id,
                "input_values": input_values,
                "widgets": widgets,
                "total_execution_time_ms": total_execution_time_ms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dashboard_render_response_input_values import DashboardRenderResponseInputValues
        from ..models.widget_render_result import WidgetRenderResult

        d = dict(src_dict)
        dashboard_id = d.pop("dashboard_id")

        input_values = DashboardRenderResponseInputValues.from_dict(d.pop("input_values"))

        widgets = []
        _widgets = d.pop("widgets")
        for widgets_item_data in _widgets:
            widgets_item = WidgetRenderResult.from_dict(widgets_item_data)

            widgets.append(widgets_item)

        total_execution_time_ms = d.pop("total_execution_time_ms")

        dashboard_render_response = cls(
            dashboard_id=dashboard_id,
            input_values=input_values,
            widgets=widgets,
            total_execution_time_ms=total_execution_time_ms,
        )

        dashboard_render_response.additional_properties = d
        return dashboard_render_response

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
