from __future__ import annotations

import re


def _login(client, email: str, password: str):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response


def _create(client, **overrides):
    payload = {
        "title": "Due date task",
        "priority": "medium",
        "due_date": "2026-12-15",
    }
    payload.update(overrides)
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    return response.get_json()


def test_create_stores_valid_due_date(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    task = _create(client, due_date="2026-11-30")
    assert task["due_date"] == "2026-11-30"

    listed = client.get("/api/tasks").get_json()
    match = next(item for item in listed if item["id"] == task["id"])
    assert match["due_date"] == "2026-11-30"


def test_create_missing_due_date_rejected(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    response = client.post(
        "/api/tasks",
        json={"title": "No due", "priority": "low"},
    )
    assert response.status_code == 400
    body = response.get_json()
    assert "due_date" in body.get("fields", {})


def test_create_malformed_due_date_rejected(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    response = client.post(
        "/api/tasks",
        json={
            "title": "Bad due",
            "priority": "low",
            "due_date": "15-11-2026",
        },
    )
    assert response.status_code == 400
    body = response.get_json()
    assert "due_date" in body.get("fields", {})
    assert "YYYY-MM-DD" in body["fields"]["due_date"]


def test_create_impossible_calendar_date_rejected(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    response = client.post(
        "/api/tasks",
        json={
            "title": "Impossible due",
            "priority": "low",
            "due_date": "2026-02-31",
        },
    )
    assert response.status_code == 400
    body = response.get_json()
    assert "due_date" in body.get("fields", {})


def test_edit_updates_due_date(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create(client, due_date="2026-12-01")
    task_id = created["id"]

    response = client.put(
        f"/api/tasks/{task_id}",
        json={
            "title": created["title"],
            "priority": created["priority"],
            "due_date": "2027-01-15",
        },
    )
    assert response.status_code == 200
    assert response.get_json()["due_date"] == "2027-01-15"


def test_viewer_cannot_change_due_date(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create(client, due_date="2026-12-01")
    task_id = created["id"]

    _login(client, "viewer@taskflow.local", "Viewer123!")
    response = client.put(
        f"/api/tasks/{task_id}",
        json={
            "title": created["title"],
            "priority": created["priority"],
            "due_date": "2027-06-01",
        },
    )
    assert response.status_code == 403

    _login(client, "dev@taskflow.local", "Dev123!")
    assert client.get(f"/api/tasks/{task_id}").get_json()["due_date"] == "2026-12-01"


def test_board_forms_use_date_inputs(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    html = client.get("/board").get_data(as_text=True)
    for input_id in ("task-due-date", "edit-task-due-date"):
        match = re.search(
            rf'<input[^>]*id="{input_id}"[^>]*>',
            html,
        )
        assert match, f"missing input {input_id}"
        tag = match.group(0)
        assert 'type="date"' in tag
        assert "required" in tag


def test_board_js_renders_due_date_indicator():
    from pathlib import Path

    board_js = Path("static/js/board.js").read_text(encoding="utf-8")
    assert "data-due-date=" in board_js
    assert "task-due-date" in board_js or "Due " in board_js
