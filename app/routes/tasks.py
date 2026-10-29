from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.auth.decorators import developer_required_api, login_required_api
from app.services.auth_service import current_user
from app.services.task_service import TaskServiceError, create_task_from_payload, get_tasks_for_board

bp = Blueprint("tasks_api", __name__, url_prefix="/api/tasks")


@bp.get("")
@login_required_api
def list_tasks_api():
    return jsonify(get_tasks_for_board()), 200


@bp.post("")
@developer_required_api
def create_task_api():
    """Developer-only create task in To Do (US05, RN02). Admin and Viewer get 403."""
    user = current_user()
    assert user is not None
    try:
        task = create_task_from_payload(
            payload=request.get_json(silent=True),
            created_by_id=user.id,
        )
    except TaskServiceError as error:
        payload: dict = {"message": error.message}
        if error.fields is not None:
            payload["fields"] = error.fields
        return jsonify(payload), error.status
    return jsonify(task), 201
