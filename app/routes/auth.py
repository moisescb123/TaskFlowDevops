from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from app.auth.decorators import login_required_api
from app.services.auth_service import (
    AuthError,
    authenticate,
    clear_session,
    current_user,
    establish_session,
    validate_login_payload,
)

bp = Blueprint("auth_api", __name__, url_prefix="/api/auth")


@bp.post("/login")
def login():
    # Clear any prior session on every login attempt (success or failure).
    clear_session()

    data = request.get_json(silent=True)
    validation_error = validate_login_payload(data)
    if validation_error is not None:
        return (
            jsonify(
                {
                    "message": validation_error.message,
                    "fields": validation_error.fields or {},
                }
            ),
            validation_error.status,
        )

    assert data is not None
    result = authenticate(str(data["email"]), str(data["password"]))
    if isinstance(result, AuthError):
        return jsonify({"message": result.message}), result.status

    establish_session(result)
    return jsonify(result.to_public_dict()), 200


@bp.get("/me")
@login_required_api
def me():
    user = current_user()
    assert user is not None
    return jsonify(user.to_public_dict()), 200


@bp.post("/logout")
@login_required_api
def logout():
    clear_session()
    return ("", 204)


@bp.get("/protected-stub")
@login_required_api
def protected_stub():
    """Test-only protected API; unavailable outside TESTING."""
    if not current_app.config.get("TESTING"):
        return jsonify({"message": "Not found"}), 404
    return jsonify({"ok": True}), 200
