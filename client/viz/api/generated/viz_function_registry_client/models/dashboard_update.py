from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dashboard_structure import DashboardStructure


T = TypeVar("T", bound="DashboardUpdate")


@_attrs_define
class DashboardUpdate:
    """Schema for updating a dashboard.

    Attributes:
        title (None | str | Unset):
        description (None | str | Unset):
        structure (DashboardStructure | None | Unset):
    """

    title: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    structure: DashboardStructure | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dashboard_structure import DashboardStructure

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

        structure: dict[str, Any] | None | Unset
        if isinstance(self.structure, Unset):
            structure = UNSET
        elif isinstance(self.structure, DashboardStructure):
            structure = self.structure.to_dict()
        else:
            structure = self.structure

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if structure is not UNSET:
            field_dict["structure"] = structure

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dashboard_structure import DashboardStructure

        d = dict(src_dict)

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

        def _parse_structure(data: object) -> DashboardStructure | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                structure_type_0 = DashboardStructure.from_dict(data)

                return structure_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DashboardStructure | None | Unset, data)

        structure = _parse_structure(d.pop("structure", UNSET))

        dashboard_update = cls(
            title=title,
            description=description,
            structure=structure,
        )

        dashboard_update.additional_properties = d
        return dashboard_update

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
