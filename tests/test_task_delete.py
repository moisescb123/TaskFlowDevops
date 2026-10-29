from __future__ import annotations

from app.models.task import get_task_by_id


def _login(client, email: str, password: str):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response


def _create_task(client, **overrides):
    payload = {
        "title": "Task to delete",
        "priority": "medium",
        "due_date": "2026-11-15",
    }
    payload.update(overrides)
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    return response.get_json()


def test_developer_deletes_task(client, app):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    task_id = created["id"]

    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 204
    assert response.data == b""

    listed = client.get("/api/tasks").get_json()
    assert all(item["id"] != task_id for item in listed)

    detail = client.get(f"/api/tasks/{task_id}")
    assert detail.status_code == 404

    with app.app_context():
        assert get_task_by_id(task_id) is None


def test_delete_missing_task_returns_404(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    response = client.delete("/api/tasks/99999")
    assert response.status_code == 404
    body = response.get_json()
    assert body["message"] == "Task not found"


def test_viewer_cannot_delete_task(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    task_id = created["id"]

    _login(client, "viewer@taskflow.local", "Viewer123!")
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 403

    _login(client, "dev@taskflow.local", "Dev123!")
    assert client.get(f"/api/tasks/{task_id}").status_code == 200


def test_admin_cannot_delete_task(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    task_id = created["id"]

    _login(client, "admin@taskflow.local", "Admin123!")
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 403


def test_anonymous_cannot_delete_task(client):
    response = client.delete("/api/tasks/1")
    assert response.status_code == 401
