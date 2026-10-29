from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
GROUPING_JS = REPO_ROOT / "static" / "js" / "board_grouping.js"


def _login(client, email: str, password: str):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response


def _seed_sample_tasks(app):
    from app.models.user import get_user_by_email
    from app.services.task_service import seed_task_for_tests

    with app.app_context():
        admin = get_user_by_email("admin@taskflow.local")
        dev = get_user_by_email("dev@taskflow.local")
        assert admin is not None and dev is not None
        seed_task_for_tests(
            title="Plan sprint",
            status="todo",
            priority="high",
            due_date="2026-11-01",
            created_by_id=admin.id,
            assignee_id=dev.id,
        )
        seed_task_for_tests(
            title="Implement board",
            status="in_progress",
            priority="medium",
            due_date="2026-11-05",
            created_by_id=dev.id,
            assignee_id=dev.id,
        )
        seed_task_for_tests(
            title="Ship login",
            status="done",
            priority="low",
            due_date="2026-10-20",
            created_by_id=dev.id,
            assignee_id=None,
        )


def test_anonymous_cannot_list_tasks(client):
    response = client.get("/api/tasks")
    assert response.status_code == 401


@pytest.mark.parametrize(
    ("email", "password"),
    [
        ("viewer@taskflow.local", "Viewer123!"),
        ("dev@taskflow.local", "Dev123!"),
        ("admin@taskflow.local", "Admin123!"),
    ],
)
def test_authenticated_can_list_tasks(client, app, email, password):
    _seed_sample_tasks(app)
    _login(client, email, password)
    response = client.get("/api/tasks")
    assert response.status_code == 200
    tasks = response.get_json()
    assert isinstance(tasks, list)
    assert len(tasks) == 3
    statuses = {task["status"] for task in tasks}
    assert statuses == {"todo", "in_progress", "done"}
    sample = tasks[0]
    for key in ("id", "title", "status", "priority", "due_date"):
        assert key in sample


def test_viewer_mutate_forbidden(client):
    _login(client, "viewer@taskflow.local", "Viewer123!")
    response = client.post("/api/tasks", json={"title": "Nope"})
    assert response.status_code == 403


def test_developer_create_stub_not_forbidden(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    response = client.post("/api/tasks", json={"title": "Later"})
    assert response.status_code == 501


def test_board_page_has_columns_for_viewer(client, app):
    _seed_sample_tasks(app)
    _login(client, "viewer@taskflow.local", "Viewer123!")
    response = client.get("/board")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'data-status="todo"' in html
    assert 'data-status="in_progress"' in html
    assert 'data-status="done"' in html
    assert "board.js" in html
    assert "board_grouping.js" in html
    assert 'data-role="viewer"' in html
    assert "Create task" not in html or 'hidden' in html.lower() or 'data-can-mutate="false"' in html


def test_group_tasks_by_status_places_titles_under_matching_columns():
    """AC1: grouping helper puts each task under its status column (not flat list only)."""
    assert GROUPING_JS.is_file(), f"Missing grouping module: {GROUPING_JS}"
    tasks = [
        {"id": 1, "title": "Plan sprint", "status": "todo"},
        {"id": 2, "title": "Implement board", "status": "in_progress"},
        {"id": 3, "title": "Ship login", "status": "done"},
        {"id": 4, "title": "Ghost", "status": "unknown"},
    ]
    script = f"""
const {{ groupTasksByStatus }} = require({json.dumps(str(GROUPING_JS).replace(chr(92), "/"))});
const grouped = groupTasksByStatus({json.dumps(tasks)});
const summary = {{
  todo: grouped.todo.map((t) => t.title),
  in_progress: grouped.in_progress.map((t) => t.title),
  done: grouped.done.map((t) => t.title),
}};
process.stdout.write(JSON.stringify(summary));
"""
    result = subprocess.run(
        ["node", "-e", script],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["todo"] == ["Plan sprint"]
    assert summary["in_progress"] == ["Implement board"]
    assert summary["done"] == ["Ship login"]


def test_viewer_api_tasks_group_into_board_columns(client, app):
    """Seeded API payloads + grouping helper = titles under correct columns."""
    _seed_sample_tasks(app)
    _login(client, "viewer@taskflow.local", "Viewer123!")
    response = client.get("/api/tasks")
    assert response.status_code == 200
    tasks = response.get_json()
    script = f"""
const {{ groupTasksByStatus }} = require({json.dumps(str(GROUPING_JS).replace(chr(92), "/"))});
const grouped = groupTasksByStatus({json.dumps(tasks)});
const summary = {{
  todo: grouped.todo.map((t) => t.title),
  in_progress: grouped.in_progress.map((t) => t.title),
  done: grouped.done.map((t) => t.title),
}};
process.stdout.write(JSON.stringify(summary));
"""
    result = subprocess.run(
        ["node", "-e", script],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["todo"] == ["Plan sprint"]
    assert summary["in_progress"] == ["Implement board"]
    assert summary["done"] == ["Ship login"]


def test_board_hides_mutate_for_viewer_shows_for_developer(client):
    _login(client, "viewer@taskflow.local", "Viewer123!")
    viewer_html = client.get("/board").get_data(as_text=True)
    assert 'data-can-mutate="false"' in viewer_html

    client.post(
        "/api/auth/login",
        json={"email": "dev@taskflow.local", "password": "Dev123!"},
    )
    dev_html = client.get("/board").get_data(as_text=True)
    assert 'data-can-mutate="true"' in dev_html


def test_tasks_persist_across_app_restart(tmp_path):
    from app import create_app
    from app.config import Config
    from app.db import init_db
    from app.models.user import get_user_by_email
    from app.services.auth_service import seed_demo_users
    from app.services.task_service import seed_task_for_tests

    class PersistConfig(Config):
        TESTING = True
        SECRET_KEY = "persist-test"
        DATABASE_PATH = str(tmp_path / "persist.db")

    app1 = create_app(PersistConfig)
    with app1.app_context():
        init_db()
        seed_demo_users()
        admin = get_user_by_email("admin@taskflow.local")
        assert admin is not None
        seed_task_for_tests(
            title="Survives restart",
            status="todo",
            priority="high",
            due_date="2026-12-01",
            created_by_id=admin.id,
        )

    app2 = create_app(PersistConfig)
    client = app2.test_client()
    client.post(
        "/api/auth/login",
        json={"email": "viewer@taskflow.local", "password": "Viewer123!"},
    )
    response = client.get("/api/tasks")
    assert response.status_code == 200
    tasks = response.get_json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Survives restart"
    assert tasks[0]["status"] == "todo"
