from __future__ import annotations

import pytest


def _login(client, email: str, password: str):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response


def _valid_payload(**overrides):
    payload = {
        "title": "Write acceptance tests",
        "priority": "high",
        "due_date": "2026-11-15",
    }
    payload.update(overrides)
    return payload


def test_developer_creates_task_in_todo(client, app):
    _login(client, "dev@taskflow.local", "Dev123!")
    response = client.post("/api/tasks", json=_valid_payload())
    assert response.status_code == 201
    task = response.get_json()
    assert task["title"] == "Write acceptance tests"
    assert task["priority"] == "high"
    assert task["due_date"] == "2026-11-15"
    assert task["status"] == "todo"
    assert task["assignee_id"] is None
    assert "id" in task

    listed = client.get("/api/tasks")
    assert listed.status_code == 200
    ids = {item["id"] for item in listed.get_json()}
    assert task["id"] in ids


@pytest.mark.parametrize(
    "payload",
    [
        {"priority": "high", "due_date": "2026-11-15"},
        {"title": "Missing priority", "due_date": "2026-11-15"},
        {"title": "Missing due", "priority": "medium"},
        {"title": "  ", "priority": "low", "due_date": "2026-11-15"},
        {"title": "Bad priority", "priority": "urgent", "due_date": "2026-11-15"},
        {"title": "Bad date", "priority": "low", "due_date": "15-11-2026"},
    ],
)
def test_create_task_rn02_validation(client, app, payload):
    _login(client, "dev@taskflow.local", "Dev123!")
    before = client.get("/api/tasks").get_json()
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 400
    body = response.get_json()
    assert body["message"] == "Validation failed"
    assert "fields" in body
    after = client.get("/api/tasks").get_json()
    assert len(after) == len(before)


def test_viewer_cannot_create_task(client):
    _login(client, "viewer@taskflow.local", "Viewer123!")
    response = client.post("/api/tasks", json=_valid_payload())
    assert response.status_code == 403


def test_admin_cannot_create_task(client):
    _login(client, "admin@taskflow.local", "Admin123!")
    response = client.post("/api/tasks", json=_valid_payload())
    assert response.status_code == 403


def test_anonymous_cannot_create_task(client):
    response = client.post("/api/tasks", json=_valid_payload())
    assert response.status_code == 401


def test_create_task_with_assignee(client, app):
    from app.models.user import get_user_by_email

    with app.app_context():
        dev = get_user_by_email("dev@taskflow.local")
        assert dev is not None
        assignee_id = dev.id

    _login(client, "dev@taskflow.local", "Dev123!")
    response = client.post(
        "/api/tasks",
        json=_valid_payload(assignee_id=assignee_id, title="Assigned work"),
    )
    assert response.status_code == 201
    task = response.get_json()
    assert task["assignee_id"] == assignee_id
    assert task["assignee_name"] == "Demo Developer"


def test_create_task_invalid_assignee(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    response = client.post("/api/tasks", json=_valid_payload(assignee_id=99999))
    assert response.status_code == 400
    body = response.get_json()
    assert "assignee_id" in body.get("fields", {})


def test_created_task_persists_across_restart(tmp_path):
    from app import create_app
    from app.config import Config
    from app.db import init_db
    from app.services.auth_service import seed_demo_users

    class PersistConfig(Config):
        TESTING = True
        SECRET_KEY = "us05-persist"
        DATABASE_PATH = str(tmp_path / "us05.db")

    app1 = create_app(PersistConfig)
    with app1.app_context():
        init_db()
        seed_demo_users()

    client1 = app1.test_client()
    client1.post(
        "/api/auth/login",
        json={"email": "dev@taskflow.local", "password": "Dev123!"},
    )
    created = client1.post("/api/tasks", json=_valid_payload(title="Survives create"))
    assert created.status_code == 201
    task_id = created.get_json()["id"]

    app2 = create_app(PersistConfig)
    client2 = app2.test_client()
    client2.post(
        "/api/auth/login",
        json={"email": "viewer@taskflow.local", "password": "Viewer123!"},
    )
    response = client2.get("/api/tasks")
    assert response.status_code == 200
    tasks = response.get_json()
    match = next(t for t in tasks if t["id"] == task_id)
    assert match["title"] == "Survives create"
    assert match["status"] == "todo"


def test_board_create_controls_for_developer(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    html = client.get("/board").get_data(as_text=True)
    assert 'data-can-create="true"' in html
    assert 'id="create-task-button"' in html
    assert "disabled" not in html.split('id="create-task-button"', 1)[1].split(">", 1)[0]
    assert 'id="create-task-form"' in html or 'id="create-task-dialog"' in html


def test_admin_board_hides_create_controls(client):
    _login(client, "admin@taskflow.local", "Admin123!")
    html = client.get("/board").get_data(as_text=True)
    assert 'data-can-create="false"' in html
    assert 'id="create-task-dialog"' not in html
    assert 'id="create-task-form"' not in html


def test_board_js_guards_duplicate_create_submit():
    from pathlib import Path

    source = (Path(__file__).resolve().parents[1] / "static" / "js" / "board.js").read_text(
        encoding="utf-8"
    )
    assert "createInFlight" in source
    assert "if (!form || createInFlight)" in source
    assert "submitBtn.disabled = true" in source
