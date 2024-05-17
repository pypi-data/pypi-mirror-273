import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetConcurrencyIntervalsResponse200RunningJobsItem")


@_attrs_define
class GetConcurrencyIntervalsResponse200RunningJobsItem:
    """
    Attributes:
        job_id (Union[Unset, str]):
        concurrency_key (Union[Unset, str]):
        started_at (Union[Unset, datetime.datetime]):
    """

    job_id: Union[Unset, str] = UNSET
    concurrency_key: Union[Unset, str] = UNSET
    started_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_id = self.job_id
        concurrency_key = self.concurrency_key
        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if concurrency_key is not UNSET:
            field_dict["concurrency_key"] = concurrency_key
        if started_at is not UNSET:
            field_dict["started_at"] = started_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        job_id = d.pop("job_id", UNSET)

        concurrency_key = d.pop("concurrency_key", UNSET)

        _started_at = d.pop("started_at", UNSET)
        started_at: Union[Unset, datetime.datetime]
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        get_concurrency_intervals_response_200_running_jobs_item = cls(
            job_id=job_id,
            concurrency_key=concurrency_key,
            started_at=started_at,
        )

        get_concurrency_intervals_response_200_running_jobs_item.additional_properties = d
        return get_concurrency_intervals_response_200_running_jobs_item

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
