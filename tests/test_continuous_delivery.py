"""Structural checks for continuous delivery after green CI (US15 / RN03)."""

from __future__ import annotations

import re
from pathlib import Path


CD_WORKFLOW = Path(".github/workflows/cd.yml")
CI_WORKFLOW = Path(".github/workflows/ci.yml")
PROCFILE = Path("Procfile")
WSGI = Path("wsgi.py")
RENDER_YAML = Path("render.yaml")
DEV_GUIDE = Path("docs/development_guide.md")
CD_DOC = Path("docs/continuous-delivery.md")


def _cd_text() -> str:
    assert CD_WORKFLOW.is_file(), "CD workflow file is missing"
    return CD_WORKFLOW.read_text(encoding="utf-8")


def test_cd_workflow_and_host_artifacts_exist():
    assert CD_WORKFLOW.is_file()
    assert PROCFILE.is_file()
    assert WSGI.is_file()
    assert RENDER_YAML.is_file()


def test_cd_runs_only_after_successful_ci_on_main():
    text = _cd_text()
    assert "workflow_run:" in text
    assert 'workflows: ["CI"]' in text or "workflows:\n      - CI" in text
    assert "types:" in text
    assert "completed" in text
    assert "success" in text
    assert "main" in text
    # Manual dispatch would bypass green-CI gating (RN03).
    assert "workflow_dispatch" not in text


def test_ci_workflow_name_matches_cd_trigger():
    ci = CI_WORKFLOW.read_text(encoding="utf-8")
    assert "name: CI" in ci


def test_no_deploy_secrets_committed_in_workflows_or_env_examples():
    """AC4: credentials live in Actions secrets / host env, not the git tree."""
    scanned = [
        CD_WORKFLOW,
        CI_WORKFLOW,
        Path(".env.example"),
        RENDER_YAML,
    ]
    secretish = re.compile(
        r"(api[_-]?key|token|secret|password|deploy[_-]?hook)\s*[:=]\s*['\"]?[^\s'\"#]{12,}",
        re.IGNORECASE,
    )
    for path in scanned:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        # Allow placeholder names / secret references, not literal hook URLs or tokens.
        assert "https://api.render.com/deploy/" not in text
        assert "rnd_" not in text.lower()
        for match in secretish.finditer(text):
            snippet = match.group(0).lower()
            assert "secrets." in text.lower() or "replace" in snippet or "generate" in snippet or "example" in snippet or "${{" in text


def test_development_guide_documents_us15_continuous_delivery():
    text = DEV_GUIDE.read_text(encoding="utf-8")
    assert "Continuous delivery (US15)" in text
    assert "RENDER_DEPLOY_HOOK" in text
    assert CD_DOC.is_file()
