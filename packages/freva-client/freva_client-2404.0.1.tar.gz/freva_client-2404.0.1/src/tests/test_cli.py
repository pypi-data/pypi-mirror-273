"""Tests for the commandline interface."""

import json

from freva_client.cli import app
from pytest import LogCaptureFixture
from typer.testing import CliRunner


def test_overview(cli_runner: CliRunner) -> None:
    """Test the overview sub command."""
    res = cli_runner.invoke(app, ["data-overview", "--host", "localhost:8080"])
    assert res.exit_code == 0
    assert res.stdout


def test_search_files(cli_runner: CliRunner) -> None:
    """Test searching for files."""
    res = cli_runner.invoke(app, ["data-search", "--host", "localhost:8080"])
    assert res.exit_code == 0
    assert res.stdout
    res = cli_runner.invoke(
        app,
        [
            "data-search",
            "--host",
            "localhost:8080",
            "project=cmip6",
            "project=bar",
            "model=foo",
        ],
    )
    assert res.exit_code == 0
    assert not res.stdout
    res = cli_runner.invoke(app, ["data-search", "--host", "localhost:8080", "--json"])
    assert res.exit_code == 0
    assert isinstance(json.loads(res.stdout), list)


def test_metadata_search(cli_runner: CliRunner) -> None:
    """Test the metadata-search sub command."""
    res = cli_runner.invoke(app, ["metadata-search", "--host", "localhost:8080"])
    assert res.exit_code == 0
    assert res.stdout
    res = cli_runner.invoke(
        app, ["metadata-search", "--host", "localhost:8080", "model=bar"]
    )
    assert res.exit_code == 0
    assert res.stdout
    res = cli_runner.invoke(
        app, ["metadata-search", "--host", "localhost:8080", "--json"]
    )
    assert res.exit_code == 0
    output = json.loads(res.stdout)
    assert isinstance(output, dict)
    res = cli_runner.invoke(
        app,
        ["metadata-search", "--host", "localhost:8080", "--json", "model=b"],
    )
    assert res.exit_code == 0
    assert isinstance(json.loads(res.stdout), dict)


def test_count_values(cli_runner: CliRunner) -> None:
    """Test the count sub command."""
    res = cli_runner.invoke(app, ["data-count", "--host", "localhost:8080"])
    assert res.exit_code == 0
    assert res.stdout
    res = cli_runner.invoke(app, ["data-count", "--host", "localhost:8080", "--json"])
    assert res.exit_code == 0
    assert isinstance(json.loads(res.stdout), int)

    res = cli_runner.invoke(app, ["data-count", "*", "--host", "localhost:8080"])
    assert res.exit_code == 0
    assert res.stdout
    res = cli_runner.invoke(
        app,
        [
            "data-count",
            "--facet",
            "ocean",
            "--host",
            "localhost:8080",
            "--json",
            "-d",
        ],
    )
    assert res.exit_code == 0
    assert isinstance(json.loads(res.stdout), dict)
    res = cli_runner.invoke(
        app, ["data-count", "--facet", "ocean", "--host", "localhost:8080", "-d"]
    )
    assert res.exit_code == 0
    assert res.stdout
    res = cli_runner.invoke(
        app,
        [
            "data-count",
            "--facet",
            "ocean",
            "--host",
            "localhost:8080",
            "realm=atmos",
            "--json",
        ],
    )
    assert res.exit_code == 0
    assert json.loads(res.stdout) == 0


def test_failed_command(cli_runner: CliRunner, caplog: LogCaptureFixture) -> None:
    """Test the handling of bad commands."""
    for cmd in ("data-count", "data-search", "metadata-search"):
        caplog.clear()
        res = cli_runner.invoke(app, [cmd, "--host", "localhost:8080", "foo=b"])
        assert res.exit_code == 0
        assert caplog.records
        assert caplog.records[-1].levelname == "WARNING"
        res = cli_runner.invoke(app, [cmd, "--host", "localhost:8080", "-f", "foo"])
        assert res.exit_code != 0
        caplog.clear()
        res = cli_runner.invoke(app, [cmd, "--host", "foo"])
        assert res.exit_code != 0
        assert caplog.records
        assert caplog.records[-1].levelname == "ERROR"
        res = cli_runner.invoke(app, [cmd, "--host", "foo", "-vvvvv"])
        assert res.exit_code != 0
        assert caplog.records
        assert caplog.records[-1].levelname == "ERROR"


def test_check_versions(cli_runner: CliRunner) -> None:
    """Check the versions."""
    for cmd in ("data-count", "data-search", "metadata-search"):
        res = cli_runner.invoke(app, [cmd, "-V"])
        assert res.exit_code == 0
