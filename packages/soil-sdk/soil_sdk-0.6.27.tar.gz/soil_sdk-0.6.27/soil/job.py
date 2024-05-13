"""Job module"""

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TypedDict, cast, overload

from soil import data, errors
from soil.api import create_experiment, get_experiment, get_state, set_state
from soil.data_structure import DataStructure
from soil.data_structure import DataStructure as InternalDataStructure
from soil.types import ExperimentStatuses as Statuses
from soil.types import Job

_DEFAULT_JOB_COLLECTION = "__default_job_collection"


class _JobDict(TypedDict):
    """Represents a Job."""

    experiment_id: str
    result_id: str
    created_at: str


class _JobGroup(TypedDict):
    """Represents a Job Group."""

    jobs: list[_JobDict]
    id: str
    created_at: str
    updated_at: str


class _Collection(TypedDict):
    job_groups: list[_JobGroup]


@dataclass(kw_only=True, slots=True)
class _Job(Job):
    """Represents a Job."""

    experiment_id: str
    result_id: str
    _created_at: str
    _group: str

    @property
    def group(self) -> str:
        """Get the group of the job"""
        return self._group

    @property
    def created_at(self) -> str:
        """Get the created at of the job"""
        return self._created_at

    @property
    def status(self) -> Statuses:
        """Get the status of the job"""
        experiment = get_experiment(self.experiment_id)
        output_key = next(
            output_key
            for (output_key, output_id) in experiment["outputs"].items()
            if output_id == self.result_id
        )
        return experiment["status"][output_key]

    @property
    def data(self) -> DataStructure:  # type:ignore[reportIncompatibleMethodOverride]
        """Get the data of the job"""
        return data(self.result_id)


@overload
def job(
    *, group: str | None = None, collection: str = _DEFAULT_JOB_COLLECTION
) -> list[Job]:
    ...


@overload
def job(
    data_object: DataStructure, *, group: str, collection: str = _DEFAULT_JOB_COLLECTION
) -> Job:
    ...


def _new_job(
    data_structure: InternalDataStructure,
    group: str,
    collection: str,
) -> Job:
    if data_structure.pipeline is None:
        raise ValueError("Pipeline plan is required")
    experiment = create_experiment(data_structure.pipeline.plan)
    state_id = None
    try:
        (state, state_id) = cast(tuple[_Collection, str], get_state(collection))
    except errors.ObjectNotFound:
        state: _Collection = {"job_groups": []}
    now = datetime.now(tz=UTC).isoformat()
    try:
        selected_group = next(
            (
                job_group
                for job_group in state["job_groups"]
                if job_group["id"] == group
            ),
        )
    except StopIteration:
        selected_group: _JobGroup = {
            "jobs": [],
            "id": group,
            "created_at": now,
            "updated_at": now,
        }
        state["job_groups"].append(selected_group)
    if data_structure.sym_id is None:
        raise ValueError("sym_id is required")
    selected_group["jobs"].append(
        {
            "experiment_id": experiment["_id"],
            "result_id": experiment["outputs"][data_structure.sym_id],
            "created_at": now,
        }
    )
    selected_group["updated_at"] = now
    set_state(collection, state, state_id=state_id)
    if data_structure.sym_id is None:
        raise ValueError("sym_id is required")
    return _Job(
        experiment_id=experiment["_id"],
        result_id=experiment["outputs"][data_structure.sym_id],
        _created_at=datetime.fromtimestamp(
            experiment["created_at"] / 1000, tz=UTC
        ).isoformat(),
        _group=group,
    )


def job(
    data_object: DataStructure | None = None,
    *,
    group: str | None = None,
    collection: str = _DEFAULT_JOB_COLLECTION,
) -> Job | list[Job] | list[list[Job]]:
    """Creates a non-blocking job at soil."""
    if data_object is not None:
        if group is None:
            raise ValueError("Group is required when creating a job with a data object")
        return _new_job(data_object, group=group, collection=collection)
    try:
        state, _ = cast(tuple[_Collection, str], get_state(collection))
    except errors.ObjectNotFound as e:
        raise errors.JobCollectionNotFound(
            f"Job collection {collection} not found."
        ) from e
    if group is not None:
        raw_jobs = next(
            (
                job_group["jobs"]
                for job_group in state["job_groups"]
                if job_group["id"] == group
            ),
            [],
        )
        return [
            _Job(
                experiment_id=job["experiment_id"],
                result_id=job["result_id"],
                _created_at=job["created_at"],
                _group=group,
            )
            for job in raw_jobs
        ]

    jobs: list[Job] = []
    for job_group in state["job_groups"]:
        for job in job_group["jobs"]:
            jobs.append(
                _Job(
                    experiment_id=job["experiment_id"],
                    result_id=job["result_id"],
                    _created_at=job["created_at"],
                    _group=job_group["id"],
                )
            )
    return jobs
