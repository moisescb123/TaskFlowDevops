from __future__ import annotations

import pytest


def _login(client, email: str, password: str):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response


def _session_set_cookie_headers(response) -> list[str]:
    return [
        header
        for header in response.headers.getlist("Set-Cookie")
        if header.lower().startswith("session=")
    ]


@pytest.mark.parametrize(
    ("email", "password", "role"),
    [
        ("admin@taskflow.local", "Admin123!", "admin"),
        ("dev@taskflow.local", "Dev123!", "developer"),
        ("viewer@taskflow.local", "Viewer123!", "viewer"),
    ],
)
def test_authenticated_logout_clears_session(client, email, password, role):
    login = _login(client, email, password)
    assert login.get_json()["role"] == role
    assert client.get("/api/auth/me").status_code == 200

    logout = client.post("/api/auth/logout")
    assert logout.status_code == 204
    assert logout.data == b""

    session_cookies = _session_set_cookie_headers(logout)
    assert session_cookies, "logout must expire the session cookie"
    joined = "; ".join(session_cookies).lower()
    assert "max-age=0" in joined
    assert client.get_cookie("session") is None

    me = client.get("/api/auth/me")
    assert me.status_code == 401

    board = client.get("/board", follow_redirects=False)
    assert board.status_code == 302
    assert "/login" in board.headers["Location"]


def test_unauthenticated_logout_returns_401(client):
    response = client.post("/api/auth/logout")
    assert response.status_code == 401
    assert "Unauthorized" in response.get_json()["message"]


def test_logout_control_present_on_board_and_admin(client):
    _login(client, "dev@taskflow.local", "Dev123!")
    board = client.get("/board")
    assert board.status_code == 200
    html = board.get_data(as_text=True)
    assert 'id="logout-button"' in html
    assert "logout.js" in html

    client.post(
        "/api/auth/login",
        json={"email": "admin@taskflow.local", "password": "Admin123!"},
    )
    admin = client.get("/admin/users")
    assert admin.status_code == 200
    admin_html = admin.get_data(as_text=True)
    assert 'id="logout-button"' in admin_html
    assert "logout.js" in admin_html
