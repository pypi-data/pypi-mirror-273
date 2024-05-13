import unittest
from dataclasses import dataclass
from datetime import UTC, datetime
from json import dumps, loads
from unittest.mock import Mock, patch
from urllib.parse import parse_qs, urlparse

from soil import errors, job
from soil.api import get_state, set_state
from soil.job import _DEFAULT_JOB_COLLECTION
from soil.types import Experiment


class TestJob(unittest.TestCase):
    @patch("soil.job.get_state")
    @patch("soil.job.get_experiment")
    def test_job_get_all(self, mock_experiment: Mock, mock_state: Mock):
        mock_state.return_value = (
            {
                "job_groups": [
                    {
                        "id": "job_group1",
                        "jobs": [
                            {
                                "experiment_id": "experiment1",
                                "result_id": "result1",
                                "created_at": "2022-01-01T00:00:00Z",
                                "updated_at": "2022-01-01T00:00:00Z",
                            },
                            {
                                "experiment_id": "experiment2",
                                "result_id": "result2",
                                "created_at": "2022-01-01T00:00:00Z",
                                "updated_at": "2022-01-01T00:00:00Z",
                            },
                        ],
                        "created_at": "2022-01-01T00:00:00Z",
                        "updated_at": "2022-01-01T00:00:00Z",
                    },
                    {
                        "id": "job_group2",
                        "jobs": [
                            {
                                "experiment_id": "experiment3",
                                "result_id": "result3",
                                "created_at": "2022-01-01T00:00:00Z",
                                "updated_at": "2022-01-01T00:00:00Z",
                            }
                        ],
                        "created_at": "2022-01-01T00:00:00Z",
                        "updated_at": "2022-01-01T00:00:00Z",
                    },
                ],
            },
            "mock",
        )
        jobs = job()
        self.assertEqual(len(jobs), 3)
        self.assertEqual(jobs[0].group, "job_group1")
        self.assertEqual(jobs[1].group, "job_group1")
        self.assertEqual(jobs[2].group, "job_group2")
        mock_experiment.return_value = Experiment(
            _id="experiment1",
            status={"abcd": "DONE"},
            experiment_status="DONE",
            app_id="my_app",
            created_at=1708591808811,
            outputs={"abcd": "result1"},
        )
        self.assertEqual("DONE", jobs[0].status)

    @patch("soil.job.get_state")
    def test_job_get_group(self, mock_state: Mock):
        mock_state.return_value = (
            {
                "job_groups": [
                    {
                        "id": "job_group1",
                        "jobs": [
                            {
                                "experiment_id": "experiment1",
                                "result_id": "result1",
                                "created_at": "2022-01-01T00:00:00Z",
                            },
                            {
                                "experiment_id": "experiment2",
                                "result_id": "result2",
                                "created_at": "2022-01-01T00:00:00Z",
                            },
                        ],
                        "created_at": "2022-01-01T00:00:00Z",
                        "updated_at": "2022-01-01T00:00:00Z",
                    },
                    {
                        "id": "job_group2",
                        "jobs": [
                            {
                                "experiment_id": "experiment3",
                                "result_id": "result3",
                                "created_at": "2022-01-01T00:00:00Z",
                            }
                        ],
                        "created_at": "2022-01-01T00:00:00Z",
                        "updated_at": "2022-01-01T00:00:00Z",
                    },
                ],
            },
            "mock",
        )
        jobs = job(group="job_group1")
        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0].group, "job_group1")
        self.assertEqual(jobs[1].group, "job_group1")

    @patch("soil.job.get_state")
    def test_job_get_invalid_collection(self, mock_state: Mock):
        def raise_exc(*_args, **_kwargs):
            raise errors.ObjectNotFound

        mock_state.side_effect = raise_exc
        with self.assertRaises(errors.JobCollectionNotFound):
            job(group="job_group1", collection="invalid")

    @patch("soil.job.datetime")
    @patch("soil.job.create_experiment")
    @patch("soil.job.get_state")
    @patch("soil.job.set_state")
    def test_job_create(
        self,
        mock_set_state: Mock,
        mock_get_state: Mock,
        mock_create_experiment: Mock,
        mock_datetime: Mock,
    ):
        now = datetime.now(UTC).isoformat()
        mock_datetime.now().isoformat.return_value = now
        mock_create_experiment.return_value = Experiment(
            _id="my_experiment",
            status={"my_output": "DONE"},
            experiment_status="DONE",
            app_id="my_app",
            outputs={"my_datastructure": "my_output"},
            created_at=1640995200 * 1000,
        )
        mock_get_state.return_value = (
            {
                "job_groups": [
                    {
                        "id": "job_group1",
                        "jobs": [
                            {
                                "experiment_id": "experiment2",
                                "result_id": "result2",
                                "created_at": "2022-01-01T00:00:00Z",
                            }
                        ],
                        "created_at": "2022-01-01T00:00:00Z",
                        "updated_at": "2022-01-01T00:00:00Z",
                    }
                ],
            },
            "mock",
        )
        my_job = job(data_object=Mock(sym_id="my_datastructure"), group="job_group1")
        self.assertEqual(my_job.group, "job_group1")
        mock_set_state.assert_called_once_with(
            _DEFAULT_JOB_COLLECTION,
            {
                "job_groups": [
                    {
                        "id": "job_group1",
                        "jobs": [
                            {
                                "experiment_id": "experiment2",
                                "result_id": "result2",
                                "created_at": "2022-01-01T00:00:00Z",
                            },
                            {
                                "experiment_id": "my_experiment",
                                "result_id": "my_output",
                                "created_at": now,
                            },
                        ],
                        "created_at": "2022-01-01T00:00:00Z",
                        "updated_at": now,
                    }
                ]
            },
            state_id="mock",
        )

    @patch("soil.job.datetime")
    @patch("soil.job.create_experiment")
    @patch("soil.job.get_state")
    @patch("soil.job.set_state")
    def test_job_create_new_group(
        self,
        mock_set_state: Mock,
        mock_get_state: Mock,
        mock_create_experiment: Mock,
        mock_datetime: Mock,
    ):
        now = datetime.now(UTC).isoformat()
        mock_datetime.now().isoformat.return_value = now
        mock_create_experiment.return_value = Experiment(
            _id="my_experiment",
            status={"my_output": "DONE"},
            experiment_status="DONE",
            app_id="my_app",
            outputs={"my_datastructure": "my_output"},
            created_at=1640995200 * 1000,
        )
        mock_get_state.return_value = (
            {
                "job_groups": [
                    {
                        "id": "job_group1",
                        "jobs": [
                            {
                                "experiment_id": "experiment2",
                                "result_id": "result2",
                                "created_at": "2022-01-01T00:00:00Z",
                            }
                        ],
                        "created_at": "2022-01-01T00:00:00Z",
                        "updated_at": "2022-01-01T00:00:00Z",
                    }
                ],
            },
            "mock",
        )
        my_job = job(data_object=Mock(sym_id="my_datastructure"), group="job_group2")
        self.assertEqual(my_job.group, "job_group2")
        mock_set_state.assert_called_once_with(
            _DEFAULT_JOB_COLLECTION,
            {
                "job_groups": [
                    {
                        "id": "job_group1",
                        "jobs": [
                            {
                                "experiment_id": "experiment2",
                                "result_id": "result2",
                                "created_at": "2022-01-01T00:00:00Z",
                            },
                        ],
                        "created_at": "2022-01-01T00:00:00Z",
                        "updated_at": "2022-01-01T00:00:00Z",
                    },
                    {
                        "id": "job_group2",
                        "jobs": [
                            {
                                "experiment_id": "my_experiment",
                                "result_id": "my_output",
                                "created_at": now,
                            },
                        ],
                        "created_at": now,
                        "updated_at": now,
                    },
                ]
            },
            state_id="mock",
        )

    @patch("soil.job.datetime")
    @patch("soil.job.create_experiment")
    @patch("soil.job.get_state")
    @patch("soil.job.set_state")
    def test_job_create_new_collection(
        self,
        mock_set_state: Mock,
        mock_get_state: Mock,
        mock_create_experiment: Mock,
        mock_datetime: Mock,
    ):
        now = datetime.now(UTC).isoformat()
        mock_datetime.now().isoformat.return_value = now
        mock_create_experiment.return_value = Experiment(
            _id="my_experiment",
            status={"my_output": "DONE"},
            experiment_status="DONE",
            app_id="my_app",
            outputs={"my_datastructure": "my_output"},
            created_at=1640995200 * 1000,
        )
        mock_get_state.side_effect = errors.ObjectNotFound
        my_job = job(data_object=Mock(sym_id="my_datastructure"), group="job_group2")
        self.assertEqual(my_job.group, "job_group2")
        mock_set_state.assert_called_once_with(
            _DEFAULT_JOB_COLLECTION,
            {
                "job_groups": [
                    {
                        "id": "job_group2",
                        "jobs": [
                            {
                                "experiment_id": "my_experiment",
                                "result_id": "my_output",
                                "created_at": now,
                            },
                        ],
                        "created_at": now,
                        "updated_at": now,
                    },
                ]
            },
            state_id=None,
        )


@dataclass
class MockHttpResponse:
    """Soil configuration class"""

    status_code: int
    text: str

    def json(self) -> dict:
        return loads(self.text)


# pylint: disable=unused-argument
def mock_http_patch(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    json: dict[str, str] | None = None,
    timeout: int,
) -> MockHttpResponse:
    assert url == "http://test_host.test/v2/states/mock_id/"
    assert json == {"name": "backtest", "state": {}}
    return MockHttpResponse(status_code=200, text=dumps({"hello": json}))


# pylint: disable=unused-argument
def mock_http_post(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    json: dict[str, str] | None = None,
    timeout: int,
) -> MockHttpResponse:
    url_parts = urlparse(url)
    assert url_parts.path == "/v2/states/"
    assert json == {"name": "backtest", "state": {}}
    return MockHttpResponse(status_code=200, text=dumps({}))


# pylint: disable=unused-argument
def mock_http_get(
    url: str, *, headers: dict[str, str] | None = None, timeout: int
) -> MockHttpResponse:
    url_parts = urlparse(url)
    query_params = parse_qs(url_parts.query)
    if url_parts.path == "/v2/states/" and query_params["name"][0] == "backtest":
        return MockHttpResponse(
            status_code=200,
            text=dumps([{"_id": "mock_id", "name": "backtest", "state": "mock_state"}]),
        )
    raise Exception("mock http case not found")


class TestStatesApiCalls(unittest.TestCase):
    @patch("soil.api.session.get", side_effect=mock_http_get)
    @patch("soil.api.session.post", side_effect=mock_http_post)
    @patch("soil.api.session.patch", side_effect=mock_http_patch)
    def test_get_state(self, *_args):
        state, state_id = get_state(name="backtest")
        self.assertEqual(state, "mock_state")
        self.assertEqual(state_id, "mock_id")

    @patch("soil.api.session.get", side_effect=mock_http_get)
    @patch("soil.api.session.post", side_effect=mock_http_post)
    @patch("soil.api.session.patch", side_effect=mock_http_patch)
    def test_set_state(self, *_args):
        set_state(name="backtest", state={}, state_id="mock_id")
        set_state(name="backtest", state={}, state_id=None)
