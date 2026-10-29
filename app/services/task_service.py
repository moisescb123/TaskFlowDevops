from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from app.models.task import (
    VALID_PRIORITIES,
    Task,
    create_task,
    get_task_by_id,
    list_tasks,
    update_task,
)
from app.models.user import get_user_by_id

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class TaskServiceError(Exception):
    status: int
    message: str
    fields: dict[str, str] | None = None


def get_tasks_for_board() -> list[dict[str, Any]]:
    return [task.to_public_dict() for task in list_tasks()]


def get_task_public(task_id: int) -> dict[str, Any] | None:
    task = get_task_by_id(task_id)
    return task.to_public_dict() if task is not None else None


def _validate_due_date(due_date: str, fields: dict[str, str]) -> None:
    if not DATE_PATTERN.match(due_date):
        fields["due_date"] = "Due date must be YYYY-MM-DD"
        return
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
        _ = date.fromisoformat(due_date)
    except ValueError:
        fields["due_date"] = "Due date must be a valid calendar date"


def _parse_optional_assignee(raw: Any) -> int | None:
    if raw is None or raw == "":
        return None
    if isinstance(raw, bool):
        raise TaskServiceError(
            status=400,
            message="Validation failed",
            fields={"assignee_id": "Assignee must be a valid user id"},
        )
    try:
        return int(raw)
    except (TypeError, ValueError) as exc:
        raise TaskServiceError(
            status=400,
            message="Validation failed",
            fields={"assignee_id": "Assignee must be a valid user id"},
        ) from exc


def create_task_from_payload(
    *,
    payload: dict[str, Any] | None,
    created_by_id: int,
) -> dict[str, Any]:
    data = payload or {}
    fields: dict[str, str] = {}

    title_raw = data.get("title")
    title = title_raw.strip() if isinstance(title_raw, str) else ""
    if not title:
        fields["title"] = "Title is required"

    priority_raw = data.get("priority")
    priority = priority_raw.strip() if isinstance(priority_raw, str) else ""
    if not priority:
        fields["priority"] = "Priority is required"
    elif priority not in VALID_PRIORITIES:
        fields["priority"] = "Priority must be high, medium, or low"

    due_raw = data.get("due_date")
    due_date = due_raw.strip() if isinstance(due_raw, str) else ""
    if not due_date:
        fields["due_date"] = "Due date is required"
    else:
        _validate_due_date(due_date, fields)

    assignee_id: int | None = None
    if "assignee_id" in data and data.get("assignee_id") not in (None, ""):
        try:
            assignee_id = _parse_optional_assignee(data.get("assignee_id"))
        except TaskServiceError as exc:
            fields.update(exc.fields or {})
        else:
            if assignee_id is not None and get_user_by_id(assignee_id) is None:
                fields["assignee_id"] = "Assignee must be a registered user"

    if fields:
        raise TaskServiceError(status=400, message="Validation failed", fields=fields)

    task = create_task(
        title=title,
        status="todo",
        priority=priority,
        due_date=due_date,
        created_by_id=created_by_id,
        assignee_id=assignee_id,
    )
    return task.to_public_dict()


def update_task_from_payload(
    *,
    task_id: int,
    payload: dict[str, Any] | None,
) -> dict[str, Any]:
    existing = get_task_by_id(task_id)
    if existing is None:
        raise TaskServiceError(status=404, message="Task not found")

    data = payload or {}
    fields: dict[str, str] = {}

    title = existing.title
    if "title" in data:
        title_raw = data.get("title")
        title = title_raw.strip() if isinstance(title_raw, str) else ""
        if not title:
            fields["title"] = "Title is required"

    priority = existing.priority
    if "priority" in data:
        priority_raw = data.get("priority")
        priority = priority_raw.strip() if isinstance(priority_raw, str) else ""
        if not priority:
            fields["priority"] = "Priority is required"
        elif priority not in VALID_PRIORITIES:
            fields["priority"] = "Priority must be high, medium, or low"

    due_date = existing.due_date
    if "due_date" in data:
        due_raw = data.get("due_date")
        due_date = due_raw.strip() if isinstance(due_raw, str) else ""
        if not due_date:
            fields["due_date"] = "Due date is required"
        else:
            _validate_due_date(due_date, fields)

    assignee_id = existing.assignee_id
    if "assignee_id" in data:
        if data.get("assignee_id") in (None, ""):
            assignee_id = None
        else:
            try:
                assignee_id = _parse_optional_assignee(data.get("assignee_id"))
            except TaskServiceError as exc:
                fields.update(exc.fields or {})
            else:
                if assignee_id is not None and get_user_by_id(assignee_id) is None:
                    fields["assignee_id"] = "Assignee must be a registered user"

    if fields:
        raise TaskServiceError(status=400, message="Validation failed", fields=fields)

    updated = update_task(
        task_id=task_id,
        title=title,
        priority=priority,
        due_date=due_date,
        assignee_id=assignee_id,
    )
    if updated is None:
        raise TaskServiceError(status=404, message="Task not found")
    return updated.to_public_dict()


def seed_task_for_tests(
    *,
    title: str,
    status: str,
    priority: str,
    due_date: str,
    created_by_id: int,
    assignee_id: int | None = None,
) -> Task:
    """Insert a task for Pytest / local demos."""
    return create_task(
        title=title,
        status=status,
        priority=priority,
        due_date=due_date,
        created_by_id=created_by_id,
        assignee_id=assignee_id,
    )
