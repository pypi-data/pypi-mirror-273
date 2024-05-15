"""Test Results API."""

import bson
import pytest

from chime_frb_api.modules.results import Results
from chime_frb_api.workflow import Work


@pytest.fixture(scope="module")
def results():
    """Results API fixture."""
    return Results(debug=True, authentication=False, base_url="http://0.0.0.0:8005")


@pytest.fixture(scope="module")
def work():
    """Work fixture."""
    work = Work(pipeline="results", user="tester", site="chime")
    work.id = str(bson.ObjectId())
    return work


def test_deposit_bad_results(results, work):
    """Test deposit bad results."""
    with pytest.raises(AssertionError):
        results.deposit([work.payload])


def test_deposit_results(results, work):
    """Test deposit results."""
    work.status = "success"
    status = results.deposit([work.payload])
    assert status[work.pipeline] == 1

    response = results.view(
        pipeline=work.pipeline,
        query={"status": "success"},
        projection={"id": 1},
    )
    assert len(response) == 1
    assert response[0]["id"] == work.id


def test_update_results(results, work):
    """Test update results."""
    work.status = "failure"
    status = results.update([work.payload])
    assert status[work.pipeline] == 1

    response = results.view(
        pipeline=work.pipeline,
        query={"status": "failure"},
        projection={"id": 1, "status": 1},
    )

    assert len(response) == 1
    assert response[0]["id"] == work.id
    assert response[0]["status"] == work.status


def test_count(results, work):
    """Test view count."""
    response = results.count(
        pipeline=work.pipeline,
        query={"status": "success"},
    )
    assert response == 0


def test_status(results, work):
    """Test status."""
    response = results.status()
    assert response == {work.pipeline: 1}


def test_delete_results(results, work):
    """Test delete results."""
    status = results.delete_ids(work.pipeline, [work.id])
    assert status[work.pipeline] == 1

    response = results.view(
        pipeline=work.pipeline,
        query={},
        projection={"id": 1},
    )

    assert len(response) == 0


def test_get_by_count(results, work):
    """Test get_by_count method."""
    pipeline = work.pipeline
    count = 5

    work.status = "success"

    for _ in range(count):
        work.id = str(bson.ObjectId())
        results.deposit([work.payload])

    response = results.get_by_count(pipeline, count)
    assert len(response) == count

    for _ in range(3):
        work.id = str(bson.ObjectId())
        results.deposit([work.payload])

    count = 2

    response = results.get_by_count(pipeline, count)

    assert len(response) == count

    for result in response:
        assert result["pipeline"] == pipeline

    # Check if the retrieved results are in the correct order (latest first)
    for i in range(len(response) - 1):
        assert response[i]["id"] > response[i + 1]["id"]


def test_get_by_id(results, work):
    """Test get_by_id method."""
    pipeline = work.pipeline

    response = results.view(
        pipeline=pipeline,
        query={},
        projection={"id": True},
        limit=3,
    )

    ids = [d["id"] for d in response]
    response = results.get_by_id(pipeline, ids)

    assert len(response) == 3

    for result in response:
        assert result["pipeline"] == pipeline
        assert result["id"] in ids


def test_get_by_event(results, work):
    """Test get_by_event method."""
    pipeline = work.pipeline
    event_number = 123456789
    work.status = "success"
    work.event = [event_number]
    work.id = str(bson.ObjectId())
    payload = results.deposit([work.payload])
    assert payload[work.pipeline] == 1

    result = results.view(
        pipeline=pipeline,
        query={"event": {"$in": work.event}},
        projection={},
        limit=1,
    )

    response = results.get_by_event(pipeline, event_number)
    print(result)
    print(response)
    assert isinstance(response, list)
    assert len(response) > 0
    assert result == response


def test_lock(results, work):
    """Test lock."""
    pipeline = work.pipeline

    response = results.view(
        pipeline=pipeline,
        query={},
        projection={"id": True},
        limit=5,
    )

    ids = [d["id"] for d in response]

    results.lock(pipeline, ids)

    response = results.view(
        pipeline=pipeline,
        query={"id": {"$in": ids}},
        projection={"results.locked": 1},
    )

    assert len(response) >= 5

    for result in response:
        assert result["results"]["locked"] is True


def test_get_locked(results, work):
    """Test get_locked method."""
    pipeline = work.pipeline
    skip = 0
    count = 5

    response = results.get_locked(pipeline, skip, count)

    assert isinstance(response, list)
    assert len(response) >= count

    for event in response:
        assert event["results"]["locked"] is True
        assert "event" in event
        assert "plots" in event
        assert "products" in event
        assert "results" in event


def test_get_locked_count(results, work):
    """Test get_locked_count method."""
    pipeline = work.pipeline

    locked_count = results.get_locked_count(pipeline)
    assert isinstance(locked_count, int)
    assert locked_count >= 5


def test_unlock(results, work, monkeypatch):
    """Test unlock method."""
    pipeline = work.pipeline

    response = results.view(
        pipeline=pipeline,
        query={},
        projection={"id": True, "results.locked": True},
        limit=5,
    )

    ids = [d["id"] for d in response]

    monkeypatch.setattr("builtins.input", lambda _: work.pipeline)

    results.unlock(pipeline, ids)

    response = results.view(
        pipeline=pipeline,
        query={"id": {"$in": ids}},
        projection={},
    )

    assert len(response) >= 5

    for result in response:
        assert result["results"]["locked"] is False
