from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dashboard_structure import DashboardStructure

T = TypeVar("T", bound="DashboardCreate")


@_attrs_define
class DashboardCreate:
    """Schema for creating a dashboard.

    Attributes:
        id (str): Unique dashboard identifier
        title (str):
        structure (DashboardStructure): Complete dashboard structure.
        description (None | str | Unset):
    """

    id: str
    title: str
    structure: DashboardStructure
    description: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title = self.title

        structure = self.structure.to_dict()

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
                "structure": structure,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dashboard_structure import DashboardStructure

        d = dict(src_dict)
        id = d.pop("id")

        title = d.pop("title")

        structure = DashboardStructure.from_dict(d.pop("structure"))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        dashboard_create = cls(
            id=id,
            title=title,
            structure=structure,
            description=description,
        )

        dashboard_create.additional_properties = d
        return dashboard_create

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
