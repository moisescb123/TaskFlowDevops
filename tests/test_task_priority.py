from __future__ import annotations

import re

import pytest


def _login(client, email: str, password: str):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response


def _create(client, **overrides):
    payload = {
        "title": "Priority task",
        "priority": "medium",
        "due_date": "2026-12-01",
    }
    payload.update(overrides)
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    return response.get_json()


@pytest.mark.parametrize("priority", ["high", "medium", "low"])
def test_create_stores_valid_priority(client, priority):
    _login(client, "dev@taskflow.local", "Dev123!")
    task = _create(client, title=f"Prio {priority}", priority=priority)
    assert task["priority"] == priority

    listed = client.get("/api/tasks").get_json()
    match = next(item for item in listed if item["id"] == task["id"])
    assert match["priority"] == priority


def test_create_missing_priority_rejected(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    response = client.post(
        "/api/tasks",
        json={"title": "No priority", "due_date": "2026-12-01"},
    )
    assert response.status_code == 400
    body = response.get_json()
    assert "priority" in body.get("fields", {})


def test_create_invalid_priority_rejected(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    response = client.post(
        "/api/tasks",
        json={
            "title": "Bad priority",
            "priority": "urgent",
            "due_date": "2026-12-01",
        },
    )
    assert response.status_code == 400
    body = response.get_json()
    assert "priority" in body.get("fields", {})


def test_edit_updates_priority(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create(client, priority="low")
    task_id = created["id"]

    response = client.put(
        f"/api/tasks/{task_id}",
        json={
            "title": created["title"],
            "priority": "high",
            "due_date": created["due_date"],
        },
    )
    assert response.status_code == 200
    assert response.get_json()["priority"] == "high"


def test_viewer_cannot_change_priority(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    created = _create(client, priority="medium")
    task_id = created["id"]

    _login(client, "viewer@taskflow.local", "Viewer123!")
    response = client.put(
        f"/api/tasks/{task_id}",
        json={
            "title": created["title"],
            "priority": "high",
            "due_date": created["due_date"],
        },
    )
    assert response.status_code == 403

    _login(client, "dev@taskflow.local", "Dev123!")
    assert client.get(f"/api/tasks/{task_id}").get_json()["priority"] == "medium"


def test_board_priority_select_offers_only_enum(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    html = client.get("/board").get_data(as_text=True)
    for select_id in ("task-priority", "edit-task-priority"):
        block = re.search(
            rf'<select[^>]*id="{select_id}"[^>]*>(.*?)</select>',
            html,
            re.DOTALL,
        )
        assert block, f"missing select {select_id}"
        values = re.findall(r'<option[^>]*value="([^"]+)"', block.group(1))
        assert values == ["high", "medium", "low"]


def test_board_js_renders_priority_indicator():
    from pathlib import Path

    board_js = Path("static/js/board.js").read_text(encoding="utf-8")
    assert "data-priority=" in board_js
    assert "priority-badge" in board_js or "priorityClass" in board_js
    css = Path("static/css/app.css").read_text(encoding="utf-8")
    assert ".priority-high" in css
    assert ".priority-medium" in css
    assert ".priority-low" in css
