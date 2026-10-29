from __future__ import annotations

from typing import Any

from app.models.task import Task, create_task, list_tasks


def get_tasks_for_board() -> list[dict[str, Any]]:
    return [task.to_public_dict() for task in list_tasks()]


def seed_task_for_tests(
    *,
    title: str,
    status: str,
    priority: str,
    due_date: str,
    created_by_id: int,
    assignee_id: int | None = None,
) -> Task:
    """Insert a task for Pytest / local demos until US05 create API lands."""
    return create_task(
        title=title,
        status=status,
        priority=priority,
        due_date=due_date,
        created_by_id=created_by_id,
        assignee_id=assignee_id,
    )
