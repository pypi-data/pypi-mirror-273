from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostExternalButtonCollectRequestBody")


@_attrs_define
class PostExternalButtonCollectRequestBody:
    """
    Attributes:
        device (Union[Unset, Any]):  Example: any.
        data (Union[Unset, Any]):  Example: any.
        time (Union[Unset, Any]):  Example: any.
    """

    device: Union[Unset, Any] = UNSET
    data: Union[Unset, Any] = UNSET
    time: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        device = self.device

        data = self.data

        time = self.time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if device is not UNSET:
            field_dict["device"] = device
        if data is not UNSET:
            field_dict["data"] = data
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        device = d.pop("device", UNSET)

        data = d.pop("data", UNSET)

        time = d.pop("time", UNSET)

        post_external_button_collect_request_body = cls(
            device=device,
            data=data,
            time=time,
        )

        post_external_button_collect_request_body.additional_properties = d
        return post_external_button_collect_request_body

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
