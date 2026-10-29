from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.auth.decorators import developer_required_api, login_required_api
from app.services.auth_service import current_user
from app.services.task_service import (
    TaskServiceError,
    create_task_from_payload,
    delete_task_by_id,
    get_task_public,
    get_tasks_for_board,
    update_task_from_payload,
)

bp = Blueprint("tasks_api", __name__, url_prefix="/api/tasks")


def _error_response(error: TaskServiceError):
    payload: dict = {"message": error.message}
    if error.fields is not None:
        payload["fields"] = error.fields
    return jsonify(payload), error.status


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
        return _error_response(error)
    return jsonify(task), 201


@bp.get("/<int:task_id>")
@login_required_api
def get_task_api(task_id: int):
    task = get_task_public(task_id)
    if task is None:
        return jsonify({"message": "Task not found"}), 404
    return jsonify(task), 200


@bp.put("/<int:task_id>")
@developer_required_api
def update_task_api(task_id: int):
    """Developer-only update task fields (US06, RN02). Status changes are US09."""
    try:
        task = update_task_from_payload(
            task_id=task_id,
            payload=request.get_json(silent=True),
        )
    except TaskServiceError as error:
        return _error_response(error)
    return jsonify(task), 200


@bp.delete("/<int:task_id>")
@developer_required_api
def delete_task_api(task_id: int):
    """Developer-only hard delete task (US07)."""
    try:
        delete_task_by_id(task_id)
    except TaskServiceError as error:
        return _error_response(error)
    return ("", 204)
