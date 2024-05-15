"""Test archive."""

from copy import deepcopy
from pathlib import Path
from shutil import rmtree
from unittest.mock import patch

import pytest

from chime_frb_api.workflow import Work
from chime_frb_api.workflow.lifecycle import archive
from chime_frb_api.workflow.lifecycle.archive import ArchiveResultsError

TEST_WORK = Work(
    pipeline="test-archive-run",
    user="test",
    plots=["archive_test/some_plot.png"],
    products=["archive_test/some_product.dat"],
    site="chime",
    creation=1676399549.2184331,
    id="4r4nd0mlyg3n3r4t3dstr1ngb33pb00p",
    config={
        "archive": {
            "results": True,
            "products": "pass",
            "plots": "pass",
            "logs": "pass",
        },
    },
)


@pytest.fixture()
def directory():
    """Directory fixture."""
    directory = Path("archive_test")
    directory.mkdir(exist_ok=True)
    (directory / "some_plot.png").touch()
    (directory / "some_product.dat").touch()
    yield directory
    rmtree(directory.as_posix())


@pytest.mark.parametrize("archive_action", ["copy", "move", "delete"])
def test_exception_during_archive(archive_action, directory):
    """Test for exception raised during archive.run()."""
    assert Path("archive_test/some_product.dat").exists()
    assert Path("archive_test/some_plot.png").exists()
    work = deepcopy(TEST_WORK)
    work.config.archive.products = archive_action
    work.config.archive.plots = archive_action
    if archive_action in ["copy", "move"]:
        with patch(f"shutil.{archive_action}", side_effect=ArchiveResultsError(f"mocked archive error in {archive_action}")):
            archive.run(work, test_mode=True)
    if archive_action == "delete":
        with patch('os.remove', side_effect=ArchiveResultsError(f"mocked archive error: {archive_action}")):
            archive.run(work, test_mode=True)
    # test archive.permission()
    with patch('subprocess.run', side_effect=ArchiveResultsError(f"mocked archive error: permission")):
        archive.run(work, test_mode=True)



def test_copy_work_products_and_plots(directory):
    """Test for copy.work_products."""
    assert Path("archive_test/some_product.dat").exists()
    assert Path("archive_test/some_plot.png").exists()
    work = deepcopy(TEST_WORK)
    work.config.archive.products = "copy"
    work.config.archive.plots = "copy"
    archive.run(work, test_mode=True)

    assert Path("archive_test/some_product.dat").exists()
    assert Path("archive_test/some_plot.png").exists()

    assert Path(
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_product.dat"  # noqa: E501
    ).exists()
    assert Path(
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_plot.png"  # noqa: E501
    ).exists()

    assert work.products == [
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_product.dat"  # noqa: E501
    ]
    assert work.plots == [
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_plot.png"  # noqa: E501
    ]


def test_copy_work_products_only(directory):
    """Test for copy.work_products."""
    assert Path("archive_test/some_product.dat").exists()
    assert Path("archive_test/some_plot.png").exists()
    work = deepcopy(TEST_WORK)
    work.config.archive.products = "copy"
    archive.run(work, test_mode=True)

    assert Path("archive_test/some_product.dat").exists()
    assert Path("archive_test/some_plot.png").exists()

    assert Path(
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_product.dat"  # noqa: E501
    ).exists()
    assert not Path(
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_plot.png"  # noqa: E501
    ).exists()

    assert work.products == [
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_product.dat"  # noqa: E501
    ]
    assert work.plots == ["archive_test/some_plot.png"]


def test_copy_work_plots_only(directory):
    """Test for copy.work_products."""
    assert Path("archive_test/some_product.dat").exists()
    assert Path("archive_test/some_plot.png").exists()
    work = deepcopy(TEST_WORK)
    work.config.archive.plots = "copy"
    archive.run(work, test_mode=True)

    assert Path("archive_test/some_product.dat").exists()
    assert Path("archive_test/some_plot.png").exists()

    assert not Path(
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_product.dat"  # noqa: E501
    ).exists()
    assert Path(
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_plot.png"  # noqa: E501
    ).exists()

    assert work.products == ["archive_test/some_product.dat"]
    assert work.plots == [
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_plot.png"  # noqa: E501
    ]


def test_move_work_products_and_plots(directory):
    """Test for move.work_products."""
    assert Path("archive_test/some_product.dat").exists()
    assert Path("archive_test/some_plot.png").exists()
    work = deepcopy(TEST_WORK)
    work.config.archive.products = "move"
    work.config.archive.plots = "move"
    archive.run(work, test_mode=True)

    assert not Path("archive_test/some_product.dat").exists()
    assert not Path("archive_test/some_plot.png").exists()

    assert Path(
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_product.dat"  # noqa: E501
    ).exists()
    assert Path(
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_plot.png"  # noqa: E501
    ).exists()

    assert work.products == [
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_product.dat"  # noqa: E501
    ]
    assert work.plots == [
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_plot.png"  # noqa: E501
    ]


def test_move_work_products_only(directory):
    """Test for move.work_products."""
    assert Path("archive_test/some_product.dat").exists()
    assert Path("archive_test/some_plot.png").exists()
    work = deepcopy(TEST_WORK)
    work.config.archive.products = "move"
    archive.run(work, test_mode=True)

    assert not Path("archive_test/some_product.dat").exists()
    assert Path("archive_test/some_plot.png").exists()

    assert Path(
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_product.dat"  # noqa: E501
    ).exists()
    assert not Path(
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_plot.png"  # noqa: E501
    ).exists()

    assert work.products == [
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_product.dat"  # noqa: E501
    ]
    assert work.plots == ["archive_test/some_plot.png"]


def test_move_work_plots_only(directory):
    """Test for move.work_products."""
    assert Path("archive_test/some_product.dat").exists()
    assert Path("archive_test/some_plot.png").exists()
    work = deepcopy(TEST_WORK)
    work.config.archive.plots = "move"
    archive.run(work, test_mode=True)

    assert Path("archive_test/some_product.dat").exists()
    assert not Path("archive_test/some_plot.png").exists()

    assert not Path(
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_product.dat"  # noqa: E501
    ).exists()
    assert Path(
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_plot.png"  # noqa: E501
    ).exists()

    assert work.products == ["archive_test/some_product.dat"]
    assert work.plots == [
        "archive_test/data/chime/baseband/processed/workflow/20230214/test-archive-run/4r4nd0mlyg3n3r4t3dstr1ngb33pb00p/some_plot.png"  # noqa: E501
    ]


def test_delete_work_products_and_plots(directory):
    """Test for copy.work_products."""
    assert Path("archive_test/some_product.dat").exists()
    assert Path("archive_test/some_plot.png").exists()
    work = deepcopy(TEST_WORK)
    work.config.archive.products = "delete"
    work.config.archive.plots = "delete"
    archive.run(work, test_mode=True)

    assert not Path("archive_test/some_product.dat").exists()
    assert not Path("archive_test/some_plot.png").exists()

    assert work.products == []
    assert work.plots == []


def test_delete_work_products_only(directory):
    """Test for copy.work_products."""
    assert Path("archive_test/some_product.dat").exists()
    assert Path("archive_test/some_plot.png").exists()
    work = deepcopy(TEST_WORK)
    work.config.archive.products = "delete"
    archive.run(work, test_mode=True)

    assert not Path("archive_test/some_product.dat").exists()
    assert Path("archive_test/some_plot.png").exists()

    assert work.products == []
    assert work.plots == ["archive_test/some_plot.png"]


def test_delete_work_plots_only(directory):
    """Test for copy.work_products."""
    assert Path("archive_test/some_product.dat").exists()
    assert Path("archive_test/some_plot.png").exists()
    work = deepcopy(TEST_WORK)
    work.config.archive.plots = "delete"
    archive.run(work, test_mode=True)

    assert Path("archive_test/some_product.dat").exists()
    assert not Path("archive_test/some_plot.png").exists()

    assert work.products == ["archive_test/some_product.dat"]
    assert work.plots == []
