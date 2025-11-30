from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.execution_stage import ExecutionStage
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.component_execution_response_output_type_0 import ComponentExecutionResponseOutputType0
    from ..models.render_output import RenderOutput

T = TypeVar("T", bound="ComponentExecutionResponse")


@_attrs_define
class ComponentExecutionResponse:
    """Response from component execution.

    Attributes:
        id (int):
        component_id (int):
        status (str):
        stage (ExecutionStage): Execution stages for components.
        started_at (datetime.datetime):
        output (ComponentExecutionResponseOutputType0 | None | RenderOutput | Unset):
        error_message (None | str | Unset):
        execution_time_ms (float | None | Unset):
        memory_used_mb (float | None | Unset):
        completed_at (datetime.datetime | None | Unset):
    """

    id: int
    component_id: int
    status: str
    stage: ExecutionStage
    started_at: datetime.datetime
    output: ComponentExecutionResponseOutputType0 | None | RenderOutput | Unset = UNSET
    error_message: None | str | Unset = UNSET
    execution_time_ms: float | None | Unset = UNSET
    memory_used_mb: float | None | Unset = UNSET
    completed_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.component_execution_response_output_type_0 import ComponentExecutionResponseOutputType0
        from ..models.render_output import RenderOutput

        id = self.id

        component_id = self.component_id

        status = self.status

        stage = self.stage.value

        started_at = self.started_at.isoformat()

        output: dict[str, Any] | None | Unset
        if isinstance(self.output, Unset):
            output = UNSET
        elif isinstance(self.output, ComponentExecutionResponseOutputType0):
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

        memory_used_mb: float | None | Unset
        if isinstance(self.memory_used_mb, Unset):
            memory_used_mb = UNSET
        else:
            memory_used_mb = self.memory_used_mb

        completed_at: None | str | Unset
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        elif isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "component_id": component_id,
                "status": status,
                "stage": stage,
                "started_at": started_at,
            }
        )
        if output is not UNSET:
            field_dict["output"] = output
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if execution_time_ms is not UNSET:
            field_dict["execution_time_ms"] = execution_time_ms
        if memory_used_mb is not UNSET:
            field_dict["memory_used_mb"] = memory_used_mb
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.component_execution_response_output_type_0 import ComponentExecutionResponseOutputType0
        from ..models.render_output import RenderOutput

        d = dict(src_dict)
        id = d.pop("id")

        component_id = d.pop("component_id")

        status = d.pop("status")

        stage = ExecutionStage(d.pop("stage"))

        started_at = isoparse(d.pop("started_at"))

        def _parse_output(data: object) -> ComponentExecutionResponseOutputType0 | None | RenderOutput | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_type_0 = ComponentExecutionResponseOutputType0.from_dict(data)

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
            return cast(ComponentExecutionResponseOutputType0 | None | RenderOutput | Unset, data)

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

        def _parse_memory_used_mb(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        memory_used_mb = _parse_memory_used_mb(d.pop("memory_used_mb", UNSET))

        def _parse_completed_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = isoparse(data)

                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))

        component_execution_response = cls(
            id=id,
            component_id=component_id,
            status=status,
            stage=stage,
            started_at=started_at,
            output=output,
            error_message=error_message,
            execution_time_ms=execution_time_ms,
            memory_used_mb=memory_used_mb,
            completed_at=completed_at,
        )

        component_execution_response.additional_properties = d
        return component_execution_response

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
