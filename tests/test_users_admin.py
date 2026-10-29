from __future__ import annotations

import pytest


def _login(client, email: str, password: str):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response


def test_admin_creates_user_success(client):
    _login(client, "admin@taskflow.local", "Admin123!")
    response = client.post(
        "/api/users",
        json={
            "email": "new.dev@taskflow.local",
            "password": "NewDev123!",
            "full_name": "New Developer",
            "role": "developer",
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["email"] == "new.dev@taskflow.local"
    assert data["full_name"] == "New Developer"
    assert data["role"] == "developer"
    assert "id" in data
    assert "password" not in data
    assert "password_hash" not in data


def test_created_user_can_login_with_assigned_role(client):
    _login(client, "admin@taskflow.local", "Admin123!")
    create = client.post(
        "/api/users",
        json={
            "email": "fresh@taskflow.local",
            "password": "Fresh123!",
            "full_name": "Fresh Viewer",
            "role": "viewer",
        },
    )
    assert create.status_code == 201

    client.post("/api/auth/login", json={"email": "x", "password": "y"})
    login = client.post(
        "/api/auth/login",
        json={"email": "fresh@taskflow.local", "password": "Fresh123!"},
    )
    assert login.status_code == 200
    assert login.get_json()["role"] == "viewer"


def test_duplicate_email_rejected(client, app):
    _login(client, "admin@taskflow.local", "Admin123!")
    first = client.post(
        "/api/users",
        json={
            "email": "dup@taskflow.local",
            "password": "Dup123!",
            "full_name": "Dup One",
            "role": "viewer",
        },
    )
    assert first.status_code == 201

    from app.db import get_db

    with app.app_context():
        before = get_db().execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]

    second = client.post(
        "/api/users",
        json={
            "email": "dup@taskflow.local",
            "password": "Dup456!",
            "full_name": "Dup Two",
            "role": "developer",
        },
    )
    assert second.status_code == 400
    body = second.get_json()
    assert "email" in (body.get("fields") or {}) or "email" in body.get("message", "").lower()

    with app.app_context():
        after = get_db().execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]
    assert after == before


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {
            "email": "bad-role@taskflow.local",
            "password": "Bad123!",
            "full_name": "Bad Role",
            "role": "superuser",
        },
        {
            "email": "not-an-email",
            "password": "Bad123!",
            "full_name": "Bad Email",
            "role": "viewer",
        },
        {
            "email": "missing-name@taskflow.local",
            "password": "Bad123!",
            "full_name": "",
            "role": "viewer",
        },
        {
            "email": "missing-pass@taskflow.local",
            "password": "",
            "full_name": "No Pass",
            "role": "viewer",
        },
    ],
)
def test_create_user_validation_errors(client, payload):
    _login(client, "admin@taskflow.local", "Admin123!")
    response = client.post("/api/users", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data.get("message")
    assert "fields" in data


@pytest.mark.parametrize(
    ("email", "password"),
    [
        ("dev@taskflow.local", "Dev123!"),
        ("viewer@taskflow.local", "Viewer123!"),
    ],
)
def test_non_admin_cannot_create_user(client, email, password):
    _login(client, email, password)
    response = client.post(
        "/api/users",
        json={
            "email": "blocked@taskflow.local",
            "password": "Blocked123!",
            "full_name": "Blocked",
            "role": "viewer",
        },
    )
    assert response.status_code == 403


def test_anonymous_cannot_create_user(client):
    response = client.post(
        "/api/users",
        json={
            "email": "anon@taskflow.local",
            "password": "Anon123!",
            "full_name": "Anon",
            "role": "viewer",
        },
    )
    assert response.status_code == 401


def test_admin_lists_users_without_password_fields(client):
    _login(client, "admin@taskflow.local", "Admin123!")
    response = client.get("/api/users")
    assert response.status_code == 200
    users = response.get_json()
    assert isinstance(users, list)
    assert len(users) >= 3
    for user in users:
        assert set(user.keys()) >= {"id", "email", "full_name", "role"}
        assert "password" not in user
        assert "password_hash" not in user


@pytest.mark.parametrize(
    ("email", "password"),
    [
        ("dev@taskflow.local", "Dev123!"),
        ("viewer@taskflow.local", "Viewer123!"),
    ],
)
def test_non_admin_cannot_list_users(client, email, password):
    _login(client, email, password)
    response = client.get("/api/users")
    assert response.status_code == 403


def test_anonymous_cannot_list_users(client):
    response = client.get("/api/users")
    assert response.status_code == 401


def test_admin_users_page_includes_registration_form(client):
    _login(client, "admin@taskflow.local", "Admin123!")
    response = client.get("/admin/users")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'id="register-form"' in html
    assert 'id="users-table"' in html
    assert "admin_users.js" in html


def test_create_stores_hashed_password(client, app):
    _login(client, "admin@taskflow.local", "Admin123!")
    plain = "HashedOnly123!"
    response = client.post(
        "/api/users",
        json={
            "email": "hashed@taskflow.local",
            "password": plain,
            "full_name": "Hashed User",
            "role": "developer",
        },
    )
    assert response.status_code == 201

    from app.db import get_db

    with app.app_context():
        row = get_db().execute(
            "SELECT password_hash FROM users WHERE email = ?",
            ("hashed@taskflow.local",),
        ).fetchone()
        assert row is not None
        assert row["password_hash"] != plain
        assert ":" in row["password_hash"]
