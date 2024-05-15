"""Tests for the workflow CLI."""

import click
import logging
import pytest
from click.testing import CliRunner

from chime_frb_api.modules.buckets import Buckets
from chime_frb_api.workflow import Work
from chime_frb_api.workflow.runner import cli

BUCKETS_KWARGS = {"debug": True, "base_url": "http://localhost:8000"}
LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def buckets():
    """Create a Buckets instance."""
    buckets = Buckets(**BUCKETS_KWARGS)
    # flush any existing Work objects
    if "workflow-tests" in buckets.pipelines():
        buckets.delete_many("workflow-tests", force=True)
    yield buckets
    buckets.delete_many("workflow-tests", force=True)


@pytest.fixture()
def work():
    """Create a Work instance."""
    return Work(pipeline="workflow-tests", user="tester", site="local")


@pytest.fixture()
def work_with_command():
    """Create a Work instance."""
    return Work(
        pipeline="workflow-tests",
        user="tester",
        site="local",
        command=["echo", "{'reply': 'hello world'}"],
    )

@pytest.fixture()
def work_with_invalid_command():
    """Create a Work instance."""
    return Work(
        pipeline="workflow-tests",
        user="tester",
        site="local",
        command=["ech", "{'reply': 'hello world'}"],
    )


@pytest.fixture()
def work_with_command_and_tuple_reply():
    """Create a Work instance."""
    return Work(
        pipeline="workflow-tests",
        user="tester",
        site="local",
        command=["echo", "({'reply': 'hello world'}, ['hi'], ['there'])"],
    )


@pytest.fixture()
def work_with_stdout_cmd():
    """Create a Work instance."""
    return Work(
        pipeline="workflow-tests",
        user="tester",
        site="local",
        command=["echo", "hello world"],
    )


def invoke_run(func_name: str, lifetime: int = 1):
    """Invoke the run command with the given arguments."""
    return CliRunner().invoke(
        cli,
        [
            "run",
            "workflow-tests",
            "chime_frb_api.tests.test_workflow." + func_name,
            "--lifetime=%i" % lifetime,
            "--base-url=http://localhost:8000",
            "--site=local",
            "--sleep-time=1",
            "--loki-url=http://not-working-loki-url",
            "--log-level=INFO",
        ],
    )


def invoke_dynamic_run(lifetime: int = 1):
    """Invoke the run command with the given arguments."""
    return CliRunner().invoke(
        cli,
        [
            "run",
            "workflow-tests",
            "--lifetime=%i" % lifetime,
            "--base-url=http://localhost:8000",
            "--site=local",
            "--sleep-time=1",
            "--loki-url=http://not-working-loki-url",
            "--log-level=INFO",
        ],
    )


def test_success(buckets, work):
    """Test that a successful task is marked as such."""
    assert work.deposit(**BUCKETS_KWARGS)
    result = invoke_run("sleep_func")
    assert result.exit_code == 0
    assert buckets.status("workflow-tests")["success"] == 1


def test_multi_success(buckets, work):
    """Test that a successful task is marked as such."""
    assert work.deposit()
    assert work.deposit()
    result = invoke_run("sleep_func", lifetime=2)
    assert result.exit_code == 0
    assert buckets.status("workflow-tests")["success"] == 2


def test_timeout(buckets, work, caplog):
    """Test that a task that times out is marked as such."""
    work.parameters = {"s": 2}
    work.timeout = 1
    assert work.deposit()
    with caplog.at_level(logging.ERROR):
        result = invoke_run("sleep_func")
        assert "work timed out" in caplog.text
    assert result.exit_code == 0
    assert buckets.status("workflow-tests")["failure"] == 1


def test_failing_func(buckets, work):
    """Test that a failing task is marked as such."""
    assert work.deposit()
    result = invoke_run("failing_func")
    assert result.exit_code == 0
    assert buckets.status("workflow-tests")["failure"] == 1


def test_noncompliant_func(buckets, work):
    """Test that a noncompliant task is marked as such."""
    assert work.deposit()
    result = invoke_run("noncompliant_func")
    assert result.exit_code == 0
    assert buckets.status("workflow-tests")["failure"] == 1


def test_running_command(buckets, work_with_command):
    """Test workflow run with work.command option."""
    work_id = work_with_command.deposit(return_ids=True)
    result = invoke_dynamic_run()
    assert result.exit_code == 0
    assert buckets.view(query={"id": work_id[0]}, projection={"results": True})[0] == {
        "results": {"reply": "hello world"}
    }

def test_invalid_command(buckets, work_with_invalid_command, caplog):
    """Test workflow run with work.command option."""
    work_id = work_with_invalid_command.deposit(return_ids=True)
    with caplog.at_level(logging.ERROR):
        result = invoke_dynamic_run()
        assert "chime_frb_api.workflow.lifecycle.validate.ValidateUserFunctionError: Failed to validate work command." in caplog.text
    assert result.exit_code == 0
    assert buckets.view(query={"id": work_id[0]}, projection={"results": True})[0] == {
        "results": None
    }

def test_command_with_tuple_reply(buckets, work_with_command_and_tuple_reply):
    """Test workflow work.command option and parsing of tuple reply."""
    work_id = work_with_command_and_tuple_reply.deposit(return_ids=True)
    result = invoke_dynamic_run()
    assert result.exit_code == 0
    assert buckets.view(
        query={"id": work_id[0]},
        projection={"results": True, "plots": True, "products": True},
    )[0] == {
        "results": {"reply": "hello world"},
        "products": ["hi"],
        "plots": ["there"],
    }


def test_command_with_stdout(buckets, work_with_stdout_cmd):
    """Test workflow work.command with no format reply."""
    work_id = work_with_stdout_cmd.deposit(return_ids=True)
    result = invoke_dynamic_run()
    assert result.exit_code == 0
    assert buckets.view(query={"id": work_id[0]}, projection={"results": True})[0][
        "results"
    ]["stdout"] == ["hello world"]


def test_bad_imports(buckets, work):
    """Test that a task with bad imports is marked as such."""
    assert work.deposit()
    result = invoke_run("nonexisting_func")
    assert result.exit_code == 1
    assert buckets.status("workflow-tests")["queued"] == 1


def test_click_func(buckets, work):
    """Test that a click function can be run."""
    assert work.deposit()
    result = invoke_run("click_func")
    assert result.exit_code == 0
    assert buckets.status("workflow-tests")["success"] == 1


def test_bad_base_url():
    """Test that a bad base URL is handled correctly."""
    result = CliRunner().invoke(
        cli,
        [
            "run",
            "workflow-tests",
            "chime_frb_api.tests.test_workflow.sleep_func",
            "--lifetime=1",
            "--base-url=http://localhost:9000",
            "--site=local",
            "--sleep-time=1",
            "--loki-url=http://not-a-real-url",
            "--log-level=INFO",
        ],
    )
    assert result.exit_code == 1


def test_pipeline_deploy(requests_mock):
    """Tests workflow pipeline deploy function."""
    # ? Mocking POST requests that generated a pipeline config.
    requests_mock.post(
        "http://localhost:8006/v1/pipelines",
        json=[
            {"id": "5349b4ddd2781d08c09890f3"},
            {"id": "5349b4ddd2781d08c09890f4"},
            {"id": "5349b4ddd2781d08c09890f5"},
        ],
    )
    # ? Invoke CLI command
    result = CliRunner().invoke(
        cli,
        [
            "pipelines",
            "deploy",
            "./chime_frb_api/workflow/cli/sample.yaml",
            "-b",
            "http://localhost:8006",
        ],
    )
    assert result.exit_code == 0


def sleep_func(**kwargs):
    """Sleep for a given number of seconds."""
    from time import sleep

    sleep(kwargs.get("s", 0.1))
    return {}, [], []


def failing_func(**kwargs):
    """Raise an exception."""
    raise ValueError


def noncompliant_func(**kwargs):
    """Return a non-compliant result."""
    return True


@click.command()
@click.option("--opt", default=1)
def click_func(opt):
    """A click function."""
    return {}, [], []
