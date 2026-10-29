from __future__ import annotations

import pytest


@pytest.mark.parametrize(
    ("email", "password", "role", "full_name"),
    [
        ("admin@taskflow.local", "Admin123!", "admin", "Demo Admin"),
        ("dev@taskflow.local", "Dev123!", "developer", "Demo Developer"),
        ("viewer@taskflow.local", "Viewer123!", "viewer", "Demo Viewer"),
    ],
)
def test_login_success_returns_user_and_role(client, email, password, role, full_name):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["email"] == email
    assert data["role"] == role
    assert data["full_name"] == full_name
    assert "password" not in data
    assert "password_hash" not in data


def test_login_invalid_credentials(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@taskflow.local", "password": "wrong"},
    )
    assert response.status_code == 401
    assert "Invalid" in response.get_json()["message"]


def test_failed_login_leaves_no_session(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@taskflow.local", "password": "wrong"},
    )
    assert response.status_code == 401
    me = client.get("/api/auth/me")
    assert me.status_code == 401


def test_failed_login_clears_prior_session(client):
    ok = client.post(
        "/api/auth/login",
        json={"email": "admin@taskflow.local", "password": "Admin123!"},
    )
    assert ok.status_code == 200
    assert client.get("/api/auth/me").status_code == 200

    bad = client.post(
        "/api/auth/login",
        json={"email": "admin@taskflow.local", "password": "wrong"},
    )
    assert bad.status_code == 401
    assert client.get("/api/auth/me").status_code == 401


def test_login_missing_fields(client):
    response = client.post("/api/auth/login", json={})
    assert response.status_code == 400
    fields = response.get_json()["fields"]
    assert "email" in fields
    assert "password" in fields


def test_login_invalid_email_format(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "not-an-email", "password": "x"},
    )
    assert response.status_code == 400
    assert "email" in response.get_json()["fields"]


def test_me_authenticated(client):
    client.post(
        "/api/auth/login",
        json={"email": "dev@taskflow.local", "password": "Dev123!"},
    )
    response = client.get("/api/auth/me")
    assert response.status_code == 200
    data = response.get_json()
    assert data["role"] == "developer"
    assert "password" not in data


def test_me_unauthenticated(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_protected_stub_requires_auth(client):
    denied = client.get("/api/auth/protected-stub")
    assert denied.status_code == 401
    client.post(
        "/api/auth/login",
        json={"email": "viewer@taskflow.local", "password": "Viewer123!"},
    )
    ok = client.get("/api/auth/protected-stub")
    assert ok.status_code == 200


def test_board_redirects_when_anonymous(client):
    response = client.get("/board", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_login_page_redirects_when_authenticated(client):
    client.post(
        "/api/auth/login",
        json={"email": "admin@taskflow.local", "password": "Admin123!"},
    )
    response = client.get("/login", follow_redirects=False)
    assert response.status_code == 302
    assert "/admin/users" in response.headers["Location"]


@pytest.mark.parametrize(
    ("email", "password"),
    [
        ("dev@taskflow.local", "Dev123!"),
        ("viewer@taskflow.local", "Viewer123!"),
    ],
)
def test_non_admin_cannot_open_admin_users(client, email, password):
    client.post("/api/auth/login", json={"email": email, "password": password})
    response = client.get("/admin/users", follow_redirects=False)
    assert response.status_code == 302
    assert "/board" in response.headers["Location"]


def test_admin_can_open_admin_users(client):
    client.post(
        "/api/auth/login",
        json={"email": "admin@taskflow.local", "password": "Admin123!"},
    )
    response = client.get("/admin/users", follow_redirects=False)
    assert response.status_code == 200


def test_password_hashes_are_not_plain_text(app):
    from app.db import get_db

    with app.app_context():
        row = get_db().execute(
            "SELECT password_hash FROM users WHERE email = ?",
            ("admin@taskflow.local",),
        ).fetchone()
        assert row is not None
        assert row["password_hash"] != "Admin123!"
        assert row["password_hash"].startswith("scrypt:") or ":" in row["password_hash"]


def test_create_app_requires_secret_key_outside_testing(tmp_path):
    from app import create_app
    from app.config import Config

    class NoSecretConfig(Config):
        TESTING = False
        SECRET_KEY = None
        DATABASE_PATH = str(tmp_path / "nosecret.db")

    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        create_app(NoSecretConfig)
