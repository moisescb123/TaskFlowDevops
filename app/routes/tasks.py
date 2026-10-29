from __future__ import annotations

from flask import Blueprint, jsonify

from app.auth.decorators import login_required_api, non_viewer_required_api
from app.services.task_service import get_tasks_for_board

bp = Blueprint("tasks_api", __name__, url_prefix="/api/tasks")


@bp.get("")
@login_required_api
def list_tasks_api():
    return jsonify(get_tasks_for_board()), 200


@bp.post("")
@non_viewer_required_api
def create_task_api_stub():
    """Viewer forbidden (US04). Full create lands in US05."""
    return jsonify({"message": "Task creation is not available yet"}), 501
