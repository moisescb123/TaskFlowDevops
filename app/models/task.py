from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.db import get_db

VALID_STATUSES = frozenset({"todo", "in_progress", "done"})
VALID_PRIORITIES = frozenset({"high", "medium", "low"})

STATUS_LABELS = {
    "todo": "To Do",
    "in_progress": "In progress",
    "done": "Done",
}


@dataclass
class Task:
    id: int
    title: str
    status: str
    priority: str
    due_date: str
    assignee_id: int | None
    created_by_id: int
    created_at: str
    updated_at: str
    assignee_name: str | None = None

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date,
            "assignee_id": self.assignee_id,
            "assignee_name": self.assignee_name,
            "created_by_id": self.created_by_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


def _row_to_task(row: Any) -> Task:
    keys = row.keys()
    return Task(
        id=row["id"],
        title=row["title"],
        status=row["status"],
        priority=row["priority"],
        due_date=row["due_date"],
        assignee_id=row["assignee_id"],
        created_by_id=row["created_by_id"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        assignee_name=row["assignee_name"] if "assignee_name" in keys else None,
    )


def list_tasks() -> list[Task]:
    rows = get_db().execute(
        """
        SELECT
            t.id,
            t.title,
            t.status,
            t.priority,
            t.due_date,
            t.assignee_id,
            t.created_by_id,
            t.created_at,
            t.updated_at,
            u.full_name AS assignee_name
        FROM tasks t
        LEFT JOIN users u ON u.id = t.assignee_id
        ORDER BY t.id ASC
        """
    ).fetchall()
    return [_row_to_task(row) for row in rows]


def get_task_by_id(task_id: int) -> Task | None:
    row = get_db().execute(
        """
        SELECT
            t.id,
            t.title,
            t.status,
            t.priority,
            t.due_date,
            t.assignee_id,
            t.created_by_id,
            t.created_at,
            t.updated_at,
            u.full_name AS assignee_name
        FROM tasks t
        LEFT JOIN users u ON u.id = t.assignee_id
        WHERE t.id = ?
        """,
        (task_id,),
    ).fetchone()
    return _row_to_task(row) if row else None


def create_task(
    *,
    title: str,
    status: str,
    priority: str,
    due_date: str,
    created_by_id: int,
    assignee_id: int | None = None,
) -> Task:
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Invalid priority: {priority}")
    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO tasks (
            title, status, priority, due_date, assignee_id, created_by_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            title.strip(),
            status,
            priority,
            due_date,
            assignee_id,
            created_by_id,
        ),
    )
    db.commit()
    task = get_task_by_id(int(cursor.lastrowid))
    if task is None:
        raise RuntimeError("Failed to load created task")
    return task
