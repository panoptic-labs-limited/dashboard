from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.render_output import RenderOutput
    from ..models.widget_render_result_output_type_0 import WidgetRenderResultOutputType0


T = TypeVar("T", bound="WidgetRenderResult")


@_attrs_define
class WidgetRenderResult:
    """Result of rendering a single widget.

    Attributes:
        widget_id (str):
        component_alias (str):
        status (str):
        output (None | RenderOutput | Unset | WidgetRenderResultOutputType0):
        error_message (None | str | Unset):
        execution_time_ms (float | None | Unset):
    """

    widget_id: str
    component_alias: str
    status: str
    output: None | RenderOutput | Unset | WidgetRenderResultOutputType0 = UNSET
    error_message: None | str | Unset = UNSET
    execution_time_ms: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.render_output import RenderOutput
        from ..models.widget_render_result_output_type_0 import WidgetRenderResultOutputType0

        widget_id = self.widget_id

        component_alias = self.component_alias

        status = self.status

        output: dict[str, Any] | None | Unset
        if isinstance(self.output, Unset):
            output = UNSET
        elif isinstance(self.output, WidgetRenderResultOutputType0):
            output = self.output.to_dict()
        elif isinstance(self.output, RenderOutput):
            output = self.output.to_dict()
        else:
            output = self.output

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        execution_time_ms: float | None | Unset
        if isinstance(self.execution_time_ms, Unset):
            execution_time_ms = UNSET
        else:
            execution_time_ms = self.execution_time_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "widget_id": widget_id,
                "component_alias": component_alias,
                "status": status,
            }
        )
        if output is not UNSET:
            field_dict["output"] = output
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if execution_time_ms is not UNSET:
            field_dict["execution_time_ms"] = execution_time_ms

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.render_output import RenderOutput
        from ..models.widget_render_result_output_type_0 import WidgetRenderResultOutputType0

        d = dict(src_dict)
        widget_id = d.pop("widget_id")

        component_alias = d.pop("component_alias")

        status = d.pop("status")

        def _parse_output(data: object) -> None | RenderOutput | Unset | WidgetRenderResultOutputType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_type_0 = WidgetRenderResultOutputType0.from_dict(data)

                return output_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_type_1 = RenderOutput.from_dict(data)

                return output_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RenderOutput | Unset | WidgetRenderResultOutputType0, data)

        output = _parse_output(d.pop("output", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_execution_time_ms(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        execution_time_ms = _parse_execution_time_ms(d.pop("execution_time_ms", UNSET))

        widget_render_result = cls(
            widget_id=widget_id,
            component_alias=component_alias,
            status=status,
            output=output,
            error_message=error_message,
            execution_time_ms=execution_time_ms,
        )

        widget_render_result.additional_properties = d
        return widget_render_result

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
