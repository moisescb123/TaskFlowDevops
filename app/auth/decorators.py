from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar

from flask import jsonify, redirect, request, url_for

from app.services.auth_service import current_user

F = TypeVar("F", bound=Callable[..., Any])


def login_required_api(view: F) -> F:
    @wraps(view)
    def wrapped(*args: Any, **kwargs: Any):
        if current_user() is None:
            return jsonify({"message": "Unauthorized"}), 401
        return view(*args, **kwargs)

    return wrapped  # type: ignore[return-value]


def login_required_page(view: F) -> F:
    @wraps(view)
    def wrapped(*args: Any, **kwargs: Any):
        if current_user() is None:
            return redirect(url_for("pages.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped  # type: ignore[return-value]


def admin_required_page(view: F) -> F:
    @wraps(view)
    def wrapped(*args: Any, **kwargs: Any):
        user = current_user()
        if user is None:
            return redirect(url_for("pages.login", next=request.path))
        if user.role != "admin":
            return redirect(url_for("pages.board"))
        return view(*args, **kwargs)

    return wrapped  # type: ignore[return-value]
