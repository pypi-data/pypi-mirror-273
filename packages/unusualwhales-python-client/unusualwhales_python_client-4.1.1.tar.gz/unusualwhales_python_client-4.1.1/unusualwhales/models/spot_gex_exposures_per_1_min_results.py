from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.spot_gex_exposures_per_1_min import SpotGEXExposuresPer1Min


T = TypeVar("T", bound="SpotGEXExposuresPer1MinResults")


@_attrs_define
class SpotGEXExposuresPer1MinResults:
    """
    Attributes:
        data (Union[Unset, List['SpotGEXExposuresPer1Min']]):
    """

    data: Union[Unset, List["SpotGEXExposuresPer1Min"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.spot_gex_exposures_per_1_min import SpotGEXExposuresPer1Min

        d = src_dict.copy()
        data = []
        _data = d.pop("data", UNSET)
        for data_item_data in _data or []:
            data_item = SpotGEXExposuresPer1Min.from_dict(data_item_data)

            data.append(data_item)

        spot_gex_exposures_per_1_min_results = cls(
            data=data,
        )

        spot_gex_exposures_per_1_min_results.additional_properties = d
        return spot_gex_exposures_per_1_min_results

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
