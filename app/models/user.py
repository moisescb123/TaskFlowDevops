from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.db import get_db

VALID_ROLES = frozenset({"admin", "developer", "viewer"})


@dataclass
class User:
    id: int
    email: str
    password_hash: str
    full_name: str
    role: str

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role,
        }


def _row_to_user(row: Any) -> User:
    return User(
        id=row["id"],
        email=row["email"],
        password_hash=row["password_hash"],
        full_name=row["full_name"],
        role=row["role"],
    )


def get_user_by_email(email: str) -> User | None:
    row = get_db().execute(
        "SELECT id, email, password_hash, full_name, role FROM users WHERE email = ?",
        (email.strip().lower(),),
    ).fetchone()
    return _row_to_user(row) if row else None


def get_user_by_id(user_id: int) -> User | None:
    row = get_db().execute(
        "SELECT id, email, password_hash, full_name, role FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    return _row_to_user(row) if row else None


def list_users() -> list[User]:
    rows = get_db().execute(
        "SELECT id, email, password_hash, full_name, role FROM users ORDER BY id ASC"
    ).fetchall()
    return [_row_to_user(row) for row in rows]


def create_user(
    *,
    email: str,
    password_hash: str,
    full_name: str,
    role: str,
) -> User:
    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role: {role}")
    normalized_email = email.strip().lower()
    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO users (email, password_hash, full_name, role)
        VALUES (?, ?, ?, ?)
        """,
        (normalized_email, password_hash, full_name.strip(), role),
    )
    db.commit()
    user = get_user_by_id(int(cursor.lastrowid))
    if user is None:
        raise RuntimeError("Failed to load created user")
    return user
