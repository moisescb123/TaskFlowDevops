from __future__ import annotations

import pytest


def _login(client, email: str, password: str):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response


def _create_task(client, **overrides):
    payload = {
        "title": "Original title",
        "priority": "medium",
        "due_date": "2026-11-10",
    }
    payload.update(overrides)
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    return response.get_json()


def test_developer_updates_task(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    task_id = created["id"]

    response = client.put(
        f"/api/tasks/{task_id}",
        json={
            "title": "Updated title",
            "priority": "high",
            "due_date": "2026-12-01",
        },
    )
    assert response.status_code == 200
    task = response.get_json()
    assert task["id"] == task_id
    assert task["title"] == "Updated title"
    assert task["priority"] == "high"
    assert task["due_date"] == "2026-12-01"
    assert task["status"] == created["status"]

    listed = client.get("/api/tasks").get_json()
    match = next(item for item in listed if item["id"] == task_id)
    assert match["title"] == "Updated title"


@pytest.mark.parametrize(
    "payload",
    [
        {"title": ""},
        {"title": "   "},
        {"priority": ""},
        {"priority": "urgent"},
        {"due_date": ""},
        {"due_date": "01-12-2026"},
    ],
)
def test_update_rejects_invalid_required_fields(client, payload):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client, title="Keep me", priority="low", due_date="2026-11-11")
    task_id = created["id"]

    response = client.put(f"/api/tasks/{task_id}", json=payload)
    assert response.status_code == 400
    body = response.get_json()
    assert body["message"] == "Validation failed"
    assert "fields" in body

    current = client.get(f"/api/tasks/{task_id}")
    assert current.status_code == 200
    task = current.get_json()
    assert task["title"] == "Keep me"
    assert task["priority"] == "low"
    assert task["due_date"] == "2026-11-11"


def test_update_missing_task_returns_404(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    response = client.put(
        "/api/tasks/99999",
        json={"title": "Ghost"},
    )
    assert response.status_code == 404


def test_viewer_cannot_update_task(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    task_id = created["id"]

    _login(client, "viewer@taskflow.local", "Viewer123!")
    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Viewer edit"},
    )
    assert response.status_code == 403


def test_admin_cannot_update_task(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    task_id = created["id"]

    _login(client, "admin@taskflow.local", "Admin123!")
    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Admin edit"},
    )
    assert response.status_code == 403


def test_anonymous_cannot_update_task(client):
    response = client.put("/api/tasks/1", json={"title": "Nope"})
    assert response.status_code == 401


def test_update_assignee_and_clear(client, app):
    from app.models.user import get_user_by_email

    with app.app_context():
        dev = get_user_by_email("dev@taskflow.local")
        assert dev is not None
        assignee_id = dev.id

    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    task_id = created["id"]

    assigned = client.put(
        f"/api/tasks/{task_id}",
        json={"assignee_id": assignee_id},
    )
    assert assigned.status_code == 200
    assert assigned.get_json()["assignee_id"] == assignee_id

    cleared = client.put(
        f"/api/tasks/{task_id}",
        json={"assignee_id": None},
    )
    assert cleared.status_code == 200
    assert cleared.get_json()["assignee_id"] is None


def test_updated_task_persists_across_restart(tmp_path):
    from app import create_app
    from app.config import Config
    from app.db import init_db
    from app.services.auth_service import seed_demo_users

    class PersistConfig(Config):
        TESTING = True
        SECRET_KEY = "us06-persist"
        DATABASE_PATH = str(tmp_path / "us06.db")

    app1 = create_app(PersistConfig)
    with app1.app_context():
        init_db()
        seed_demo_users()

    client1 = app1.test_client()
    client1.post(
        "/api/auth/login",
        json={"email": "dev@taskflow.local", "password": "Dev123!"},
    )
    created = client1.post(
        "/api/tasks",
        json={
            "title": "Before edit",
            "priority": "low",
            "due_date": "2026-11-01",
        },
    )
    assert created.status_code == 201
    task_id = created.get_json()["id"]
    updated = client1.put(
        f"/api/tasks/{task_id}",
        json={"title": "After edit", "priority": "high"},
    )
    assert updated.status_code == 200

    app2 = create_app(PersistConfig)
    client2 = app2.test_client()
    client2.post(
        "/api/auth/login",
        json={"email": "viewer@taskflow.local", "password": "Viewer123!"},
    )
    response = client2.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    task = response.get_json()
    assert task["title"] == "After edit"
    assert task["priority"] == "high"
    assert task["due_date"] == "2026-11-01"


def test_board_has_edit_controls_for_developer(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    html = client.get("/board").get_data(as_text=True)
    assert 'id="edit-task-dialog"' in html
    assert 'id="edit-task-form"' in html
