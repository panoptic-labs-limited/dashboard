from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.render_output_type import RenderOutputType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.render_output_config_type_0 import RenderOutputConfigType0
    from ..models.render_output_data_type_0 import RenderOutputDataType0

T = TypeVar("T", bound="RenderOutput")


@_attrs_define
class RenderOutput:
    """Render output from a component.

    Attributes:
        type_ (RenderOutputType): Types of render outputs.
        data (RenderOutputDataType0 | str):
        config (None | RenderOutputConfigType0 | Unset):
    """

    type_: RenderOutputType
    data: RenderOutputDataType0 | str
    config: None | RenderOutputConfigType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.render_output_config_type_0 import RenderOutputConfigType0
        from ..models.render_output_data_type_0 import RenderOutputDataType0

        type_ = self.type_.value

        data: dict[str, Any] | str
        if isinstance(self.data, RenderOutputDataType0):
            data = self.data.to_dict()
        else:
            data = self.data

        config: dict[str, Any] | None | Unset
        if isinstance(self.config, Unset):
            config = UNSET
        elif isinstance(self.config, RenderOutputConfigType0):
            config = self.config.to_dict()
        else:
            config = self.config

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "data": data,
            }
        )
        if config is not UNSET:
            field_dict["config"] = config

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.render_output_config_type_0 import RenderOutputConfigType0
        from ..models.render_output_data_type_0 import RenderOutputDataType0

        d = dict(src_dict)
        type_ = RenderOutputType(d.pop("type"))

        def _parse_data(data: object) -> RenderOutputDataType0 | str:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_0 = RenderOutputDataType0.from_dict(data)

                return data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(RenderOutputDataType0 | str, data)

        data = _parse_data(d.pop("data"))

        def _parse_config(data: object) -> None | RenderOutputConfigType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                config_type_0 = RenderOutputConfigType0.from_dict(data)

                return config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RenderOutputConfigType0 | Unset, data)

        config = _parse_config(d.pop("config", UNSET))

        render_output = cls(
            type_=type_,
            data=data,
            config=config,
        )

        render_output.additional_properties = d
        return render_output

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
