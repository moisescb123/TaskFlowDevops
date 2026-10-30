"""Automated testing in CI (US13) — suite presence, CI step, local parity, RN coverage."""

from __future__ import annotations

from pathlib import Path


WORKFLOW_PATH = Path(".github/workflows/ci.yml")
PYTEST_INI = Path("pytest.ini")
TESTS_DIR = Path("tests")
DEV_GUIDE = Path("docs/development_guide.md")

# Modules that provide automated coverage for business rules (as features landed).
RN_COVERAGE_MODULES = {
    "RN01": "tests/test_task_assignee.py",
    "RN02": "tests/test_task_create.py",
    "RN04": "tests/test_task_status.py",
}


def _workflow_text() -> str:
    assert WORKFLOW_PATH.is_file(), "CI workflow file is missing"
    return WORKFLOW_PATH.read_text(encoding="utf-8")


def test_pytest_config_and_suite_exist():
    assert PYTEST_INI.is_file()
    assert "testpaths = tests" in PYTEST_INI.read_text(encoding="utf-8")
    assert TESTS_DIR.is_dir()
    suite = list(TESTS_DIR.glob("test_*.py"))
    assert len(suite) >= 1


def test_ci_runs_pytest_after_dependency_install():
    text = _workflow_text()
    install_at = text.find("pip install -r requirements.txt")
    pytest_at = text.find("run: pytest")
    assert install_at != -1, "CI must install requirements before tests"
    assert pytest_at != -1, "CI must run pytest"
    assert install_at < pytest_at, "Pytest must run after dependency install"


def test_conftest_uses_isolated_temp_database():
    conftest = (TESTS_DIR / "conftest.py").read_text(encoding="utf-8")
    assert "tmp_path" in conftest
    assert "TESTING = True" in conftest


def test_rn_business_rules_have_automated_coverage_modules():
    """AC4: RN01/RN02/RN04 covered as features landed; RN03 is US14 (branch protection)."""
    for rule, path in RN_COVERAGE_MODULES.items():
        assert Path(path).is_file(), f"{rule} coverage module missing: {path}"


def test_development_guide_documents_us13_local_parity():
    text = DEV_GUIDE.read_text(encoding="utf-8")
    assert "Automated testing (US13)" in text
    assert "pytest" in text
