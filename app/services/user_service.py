from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from typing import Any

from app.models.user import VALID_ROLES, User, create_user, get_user_by_email, list_users
from app.services.passwords import hash_password

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class UserServiceError:
    status: int
    message: str
    fields: dict[str, str] | None = None


def validate_user_create_payload(data: dict[str, Any] | None) -> UserServiceError | None:
    if not data:
        return UserServiceError(
            status=400,
            message="Validation failed",
            fields={
                "email": "Email is required",
                "password": "Password is required",
                "full_name": "Full name is required",
                "role": "Role is required",
            },
        )

    fields: dict[str, str] = {}
    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")
    role = data.get("role")

    if email is None or str(email).strip() == "":
        fields["email"] = "Email is required"
    elif not EMAIL_RE.match(str(email).strip()):
        fields["email"] = "Email format is invalid"

    if password is None or str(password) == "":
        fields["password"] = "Password is required"

    if full_name is None or str(full_name).strip() == "":
        fields["full_name"] = "Full name is required"

    if role is None or str(role).strip() == "":
        fields["role"] = "Role is required"
    elif str(role).strip() not in VALID_ROLES:
        fields["role"] = "Role must be admin, developer, or viewer"

    if fields:
        return UserServiceError(status=400, message="Validation failed", fields=fields)
    return None


def register_user(data: dict[str, Any] | None) -> User | UserServiceError:
    validation_error = validate_user_create_payload(data)
    if validation_error is not None:
        return validation_error

    email = str(data["email"]).strip().lower()
    password = str(data["password"])
    full_name = str(data["full_name"]).strip()
    role = str(data["role"]).strip()

    if get_user_by_email(email) is not None:
        return UserServiceError(
            status=400,
            message="Validation failed",
            fields={"email": "Email is already registered"},
        )

    try:
        return create_user(
            email=email,
            password_hash=hash_password(password),
            full_name=full_name,
            role=role,
        )
    except sqlite3.IntegrityError:
        return UserServiceError(
            status=400,
            message="Validation failed",
            fields={"email": "Email is already registered"},
        )


def get_users_for_admin() -> list[dict[str, Any]]:
    return [user.to_public_dict() for user in list_users()]
