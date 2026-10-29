from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from flask import session

from app.models.user import User, create_user, get_user_by_email, get_user_by_id
from app.services.passwords import hash_password, verify_password

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class AuthError:
    status: int
    message: str
    fields: dict[str, str] | None = None


def validate_login_payload(data: dict[str, Any] | None) -> AuthError | None:
    if not data:
        return AuthError(
            status=400,
            message="Validation failed",
            fields={"email": "Email is required", "password": "Password is required"},
        )
    fields: dict[str, str] = {}
    email = data.get("email")
    password = data.get("password")
    if email is None or str(email).strip() == "":
        fields["email"] = "Email is required"
    elif not EMAIL_RE.match(str(email).strip()):
        fields["email"] = "Email format is invalid"
    if password is None or str(password) == "":
        fields["password"] = "Password is required"
    if fields:
        return AuthError(status=400, message="Validation failed", fields=fields)
    return None


def authenticate(email: str, password: str) -> User | AuthError:
    user = get_user_by_email(email)
    if user is None or not verify_password(user.password_hash, password):
        return AuthError(status=401, message="Invalid email or password")
    return user


def establish_session(user: User) -> None:
    session.clear()
    session["user_id"] = user.id
    session["role"] = user.role
    session.permanent = False


def clear_session() -> None:
    session.clear()


def current_user() -> User | None:
    user_id = session.get("user_id")
    if user_id is None:
        return None
    return get_user_by_id(int(user_id))


def seed_demo_users() -> list[User]:
    """Create demo users if missing. Passwords are for local/demo only."""
    demos = [
        ("admin@taskflow.local", "Admin123!", "Demo Admin", "admin"),
        ("dev@taskflow.local", "Dev123!", "Demo Developer", "developer"),
        ("viewer@taskflow.local", "Viewer123!", "Demo Viewer", "viewer"),
    ]
    created: list[User] = []
    for email, password, full_name, role in demos:
        if get_user_by_email(email) is None:
            created.append(
                create_user(
                    email=email,
                    password_hash=hash_password(password),
                    full_name=full_name,
                    role=role,
                )
            )
    return created
