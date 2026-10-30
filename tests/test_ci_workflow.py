"""Structural checks for the GitHub Actions CI workflow (US12)."""

from __future__ import annotations

from pathlib import Path


WORKFLOW_PATH = Path(".github/workflows/ci.yml")


def _workflow_text() -> str:
    assert WORKFLOW_PATH.is_file(), "CI workflow file is missing"
    return WORKFLOW_PATH.read_text(encoding="utf-8")


def test_ci_workflow_file_exists():
    assert WORKFLOW_PATH.is_file()


def test_ci_workflow_triggers_on_push_and_pull_request():
    text = _workflow_text()
    assert "on:" in text
    assert "push:" in text
    assert "pull_request:" in text


def test_ci_workflow_checks_out_sets_up_python_and_installs_deps():
    text = _workflow_text()
    assert "actions/checkout@" in text
    assert "actions/setup-python@" in text
    assert "pip install -r requirements.txt" in text


def test_ci_workflow_runs_pytest():
    text = _workflow_text()
    assert "pytest" in text


def test_ci_workflow_names_visible_check():
    """Job display name feeds the GitHub status check (US12 / US14)."""
    text = _workflow_text()
    assert "name: CI" in text
    assert "name: Pytest" in text
