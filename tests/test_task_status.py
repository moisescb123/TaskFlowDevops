from __future__ import annotations


def _login(client, email: str, password: str):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response


def _create_task(client, **overrides):
    payload = {
        "title": "Status task",
        "priority": "medium",
        "due_date": "2026-11-25",
    }
    payload.update(overrides)
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    return response.get_json()


def _patch_status(client, task_id: int, status: str):
    return client.patch(
        f"/api/tasks/{task_id}/status",
        json={"status": status},
    )


def test_todo_to_in_progress(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    assert created["status"] == "todo"
    task_id = created["id"]

    response = _patch_status(client, task_id, "in_progress")
    assert response.status_code == 200
    task = response.get_json()
    assert task["status"] == "in_progress"

    listed = client.get("/api/tasks").get_json()
    match = next(item for item in listed if item["id"] == task_id)
    assert match["status"] == "in_progress"


def test_in_progress_to_done(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    task_id = created["id"]
    assert _patch_status(client, task_id, "in_progress").status_code == 200

    response = _patch_status(client, task_id, "done")
    assert response.status_code == 200
    assert response.get_json()["status"] == "done"


def test_todo_to_done_rejected(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    task_id = created["id"]

    response = _patch_status(client, task_id, "done")
    assert response.status_code == 400
    body = response.get_json()
    assert "status" in body.get("fields", {}) or "message" in body

    current = client.get(f"/api/tasks/{task_id}").get_json()
    assert current["status"] == "todo"


def test_backward_in_progress_to_todo(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    task_id = created["id"]
    assert _patch_status(client, task_id, "in_progress").status_code == 200

    response = _patch_status(client, task_id, "todo")
    assert response.status_code == 200
    assert response.get_json()["status"] == "todo"


def test_backward_done_to_in_progress(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    task_id = created["id"]
    assert _patch_status(client, task_id, "in_progress").status_code == 200
    assert _patch_status(client, task_id, "done").status_code == 200

    response = _patch_status(client, task_id, "in_progress")
    assert response.status_code == 200
    assert response.get_json()["status"] == "in_progress"


def test_status_missing_task_returns_404(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    response = _patch_status(client, 99999, "in_progress")
    assert response.status_code == 404


def test_viewer_cannot_change_status(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    task_id = created["id"]

    _login(client, "viewer@taskflow.local", "Viewer123!")
    response = _patch_status(client, task_id, "in_progress")
    assert response.status_code == 403

    _login(client, "dev@taskflow.local", "Dev123!")
    assert client.get(f"/api/tasks/{task_id}").get_json()["status"] == "todo"


def test_admin_cannot_change_status(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create_task(client)
    task_id = created["id"]

    _login(client, "admin@taskflow.local", "Admin123!")
    response = _patch_status(client, task_id, "in_progress")
    assert response.status_code == 403


def test_anonymous_cannot_change_status(client):
    response = _patch_status(client, 1, "in_progress")
    assert response.status_code == 401
