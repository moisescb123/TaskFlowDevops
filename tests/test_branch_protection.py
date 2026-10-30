"""Structural checks for main branch protection docs and CI check name (US14 / RN03)."""

from __future__ import annotations

from pathlib import Path


WORKFLOW_PATH = Path(".github/workflows/ci.yml")
DEV_GUIDE = Path("docs/development_guide.md")
PROTECTION_DOC = Path("docs/branch-protection.md")


def test_ci_job_display_name_is_pytest():
    """Required GitHub status check must match this job name."""
    text = WORKFLOW_PATH.read_text(encoding="utf-8")
    assert "name: Pytest" in text


def test_branch_protection_doc_requires_pytest_check():
    assert PROTECTION_DOC.is_file()
    text = PROTECTION_DOC.read_text(encoding="utf-8")
    assert "Pytest" in text
    assert "main" in text
    assert "RN03" in text


def test_development_guide_documents_us14_branch_protection():
    text = DEV_GUIDE.read_text(encoding="utf-8")
    assert "Branch protection (US14)" in text
    assert "Pytest" in text
