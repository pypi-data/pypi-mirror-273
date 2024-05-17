from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.concurrency_intervals_completed_jobs_item import ConcurrencyIntervalsCompletedJobsItem
    from ..models.concurrency_intervals_running_jobs_item import ConcurrencyIntervalsRunningJobsItem


T = TypeVar("T", bound="ConcurrencyIntervals")


@_attrs_define
class ConcurrencyIntervals:
    """
    Attributes:
        concurrency_key (str):
        running_jobs (List['ConcurrencyIntervalsRunningJobsItem']):
        completed_jobs (List['ConcurrencyIntervalsCompletedJobsItem']):
    """

    concurrency_key: str
    running_jobs: List["ConcurrencyIntervalsRunningJobsItem"]
    completed_jobs: List["ConcurrencyIntervalsCompletedJobsItem"]
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
        from ..models.concurrency_intervals_completed_jobs_item import ConcurrencyIntervalsCompletedJobsItem
        from ..models.concurrency_intervals_running_jobs_item import ConcurrencyIntervalsRunningJobsItem

        d = src_dict.copy()
        concurrency_key = d.pop("concurrency_key")

        running_jobs = []
        _running_jobs = d.pop("running_jobs")
        for running_jobs_item_data in _running_jobs:
            running_jobs_item = ConcurrencyIntervalsRunningJobsItem.from_dict(running_jobs_item_data)

            running_jobs.append(running_jobs_item)

        completed_jobs = []
        _completed_jobs = d.pop("completed_jobs")
        for completed_jobs_item_data in _completed_jobs:
            completed_jobs_item = ConcurrencyIntervalsCompletedJobsItem.from_dict(completed_jobs_item_data)

            completed_jobs.append(completed_jobs_item)

        concurrency_intervals = cls(
            concurrency_key=concurrency_key,
            running_jobs=running_jobs,
            completed_jobs=completed_jobs,
        )

        concurrency_intervals.additional_properties = d
        return concurrency_intervals

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
