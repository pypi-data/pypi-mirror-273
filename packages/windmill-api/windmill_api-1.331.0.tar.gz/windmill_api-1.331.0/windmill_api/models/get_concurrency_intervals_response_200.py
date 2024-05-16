from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_concurrency_intervals_response_200_completed_jobs_item import (
        GetConcurrencyIntervalsResponse200CompletedJobsItem,
    )
    from ..models.get_concurrency_intervals_response_200_running_jobs_item import (
        GetConcurrencyIntervalsResponse200RunningJobsItem,
    )


T = TypeVar("T", bound="GetConcurrencyIntervalsResponse200")


@_attrs_define
class GetConcurrencyIntervalsResponse200:
    """
    Attributes:
        concurrency_key (str):
        running_jobs (List['GetConcurrencyIntervalsResponse200RunningJobsItem']):
        completed_jobs (List['GetConcurrencyIntervalsResponse200CompletedJobsItem']):
    """

    concurrency_key: str
    running_jobs: List["GetConcurrencyIntervalsResponse200RunningJobsItem"]
    completed_jobs: List["GetConcurrencyIntervalsResponse200CompletedJobsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        concurrency_key = self.concurrency_key
        running_jobs = []
        for running_jobs_item_data in self.running_jobs:
            running_jobs_item = running_jobs_item_data.to_dict()

            running_jobs.append(running_jobs_item)

        completed_jobs = []
        for completed_jobs_item_data in self.completed_jobs:
            completed_jobs_item = completed_jobs_item_data.to_dict()

            completed_jobs.append(completed_jobs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "concurrency_key": concurrency_key,
                "running_jobs": running_jobs,
                "completed_jobs": completed_jobs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_concurrency_intervals_response_200_completed_jobs_item import (
            GetConcurrencyIntervalsResponse200CompletedJobsItem,
        )
        from ..models.get_concurrency_intervals_response_200_running_jobs_item import (
            GetConcurrencyIntervalsResponse200RunningJobsItem,
        )

        d = src_dict.copy()
        concurrency_key = d.pop("concurrency_key")

        running_jobs = []
        _running_jobs = d.pop("running_jobs")
        for running_jobs_item_data in _running_jobs:
            running_jobs_item = GetConcurrencyIntervalsResponse200RunningJobsItem.from_dict(running_jobs_item_data)

            running_jobs.append(running_jobs_item)

        completed_jobs = []
        _completed_jobs = d.pop("completed_jobs")
        for completed_jobs_item_data in _completed_jobs:
            completed_jobs_item = GetConcurrencyIntervalsResponse200CompletedJobsItem.from_dict(
                completed_jobs_item_data
            )

            completed_jobs.append(completed_jobs_item)

        get_concurrency_intervals_response_200 = cls(
            concurrency_key=concurrency_key,
            running_jobs=running_jobs,
            completed_jobs=completed_jobs,
        )

        get_concurrency_intervals_response_200.additional_properties = d
        return get_concurrency_intervals_response_200

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
