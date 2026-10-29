from __future__ import annotations

from flask import Blueprint, redirect, render_template, url_for

from app.auth.decorators import admin_required_page, login_required_page
from app.services.auth_service import current_user

bp = Blueprint("pages", __name__)

ROLE_LANDING = {
    "admin": "pages.admin_users",
    "developer": "pages.board",
    "viewer": "pages.board",
}


def landing_endpoint_for_role(role: str) -> str:
    return ROLE_LANDING.get(role, "pages.board")


@bp.get("/")
def index():
    user = current_user()
    if user is None:
        return redirect(url_for("pages.login"))
    return redirect(url_for(landing_endpoint_for_role(user.role)))


@bp.get("/login")
def login():
    user = current_user()
    if user is not None:
        return redirect(url_for(landing_endpoint_for_role(user.role)))
    return render_template("login.html")


@bp.get("/board")
@login_required_page
def board():
    user = current_user()
    assert user is not None
    return render_template("board.html", user=user)


@bp.get("/admin/users")
@admin_required_page
def admin_users():
    user = current_user()
    assert user is not None
    return render_template("admin_users.html", user=user)
