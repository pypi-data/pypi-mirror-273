from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.greek_exposure_by_strike_and_expiry import GreekExposureByStrikeAndExpiry


T = TypeVar("T", bound="GreekExposureByStrikeAndExpiryResults")


@_attrs_define
class GreekExposureByStrikeAndExpiryResults:
    """
    Attributes:
        data (Union[Unset, List['GreekExposureByStrikeAndExpiry']]):
    """

    data: Union[Unset, List["GreekExposureByStrikeAndExpiry"]] = UNSET
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
        from ..models.greek_exposure_by_strike_and_expiry import GreekExposureByStrikeAndExpiry

        d = src_dict.copy()
        data = []
        _data = d.pop("data", UNSET)
        for data_item_data in _data or []:
            data_item = GreekExposureByStrikeAndExpiry.from_dict(data_item_data)

            data.append(data_item)

        greek_exposure_by_strike_and_expiry_results = cls(
            data=data,
        )

        greek_exposure_by_strike_and_expiry_results.additional_properties = d
        return greek_exposure_by_strike_and_expiry_results

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
