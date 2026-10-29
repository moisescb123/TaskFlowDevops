from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.auth.decorators import admin_required_api
from app.services.user_service import (
    UserServiceError,
    get_users_for_admin,
    register_user,
)

bp = Blueprint("users_api", __name__, url_prefix="/api/users")


@bp.get("")
@admin_required_api
def list_users_api():
    return jsonify(get_users_for_admin()), 200


@bp.post("")
@admin_required_api
def create_user_api():
    data = request.get_json(silent=True)
    result = register_user(data if isinstance(data, dict) else None)
    if isinstance(result, UserServiceError):
        payload: dict = {"message": result.message}
        if result.fields is not None:
            payload["fields"] = result.fields
        return jsonify(payload), result.status
    return jsonify(result.to_public_dict()), 201
