from __future__ import annotations

from app.models.user import get_user_by_email


def _login(client, email: str, password: str):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response


def _create_task(client, **overrides):
    payload = {
        "title": "Ownership task",
        "priority": "medium",
        "due_date": "2026-11-20",
    }
    payload.update(overrides)
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    return response.get_json()


def test_developer_assigns_registered_user(client, app):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    task_id = created["id"]

    with app.app_context():
        assignee = get_user_by_email("viewer@taskflow.local")
        assert assignee is not None
        assignee_id = assignee.id
        assignee_name = assignee.full_name

    response = client.put(
        f"/api/tasks/{task_id}",
        json={"assignee_id": assignee_id},
    )
    assert response.status_code == 200
    task = response.get_json()
    assert task["assignee_id"] == assignee_id
    assert task["assignee_name"] == assignee_name


def test_developer_replaces_assignee(client, app):
    _login(client, "dev@taskflow.local", "Dev123!")
    with app.app_context():
        first = get_user_by_email("viewer@taskflow.local")
        second = get_user_by_email("admin@taskflow.local")
        assert first is not None and second is not None
        first_id = first.id
        second_id = second.id
        second_name = second.full_name

    created = _create_task(client, assignee_id=first_id)
    task_id = created["id"]
    assert created["assignee_id"] == first_id

    response = client.put(
        f"/api/tasks/{task_id}",
        json={"assignee_id": second_id},
    )
    assert response.status_code == 200
    task = response.get_json()
    assert task["assignee_id"] == second_id
    assert task["assignee_name"] == second_name


def test_invalid_assignee_rejected(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client, title="No bad FK")
    task_id = created["id"]

    response = client.put(
        f"/api/tasks/{task_id}",
        json={"assignee_id": 99999},
    )
    assert response.status_code == 400
    body = response.get_json()
    assert body["message"] == "Validation failed"
    assert "assignee_id" in body.get("fields", {})

    current = client.get(f"/api/tasks/{task_id}").get_json()
    assert current["assignee_id"] is None


def test_viewer_cannot_change_assignee(client, app):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    task_id = created["id"]
    with app.app_context():
        assignee = get_user_by_email("admin@taskflow.local")
        assert assignee is not None
        assignee_id = assignee.id

    _login(client, "viewer@taskflow.local", "Viewer123!")
    response = client.put(
        f"/api/tasks/{task_id}",
        json={"assignee_id": assignee_id},
    )
    assert response.status_code == 403


def test_developer_can_list_users_for_assignee_picker(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    response = client.get("/api/users")
    assert response.status_code == 200
    users = response.get_json()
    assert isinstance(users, list)
    assert len(users) >= 3
    emails = {user["email"] for user in users}
    assert "dev@taskflow.local" in emails
    assert "viewer@taskflow.local" in emails
    for user in users:
        assert "password_hash" not in user
        assert "id" in user
        assert "full_name" in user


def test_viewer_cannot_list_users(client):
    _login(client, "viewer@taskflow.local", "Viewer123!")
    response = client.get("/api/users")
    assert response.status_code == 403
