from typing import Optional
from fastapi import HTTPException

from ..internal.models import Priorities
from ..internal.types import Conn, TaskFilter
from .router import router

# GET /tasks/


@router.get("/", tags=["Read"])
def view_tasks(
    connection: Conn,
    title: Optional[str] = None,
    priority: Optional[Priorities] = None,
    done: Optional[bool] = None
):
    with connection.cursor() as cursor:
        filters: TaskFilter = {}

        if title is not None:
            filters["title"] = title
        if priority is not None:
            filters["priority"] = priority
        if done is not None:
            filters["done"] = done

        clause = " AND ".join(
            f"{key} = %s"
            for key, _ in filters.items()
        )

        query: str = f"""
        SELECT id,
               title,
               priority,
               done
        FROM tasks
            """

        if clause:
            query += f"\nWHERE {clause};"

        cursor.execute(
            query,  # type: ignore
            [val for _, val in filters.items()]
        )

        return {
            "tasks": cursor.fetchall()
        }


# GET /tasks/{_id}
@router.get("/{_id:int}", tags=["Read"])
def view_task(_id: int, connection: Conn):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id,
                   title,
                   priority,
                   done
            FROM tasks 
            WHERE id = %s;
            """,
            [_id]
        )

        rows = cursor.fetchone()

        if not rows:
            raise HTTPException(404, f"No task with ID {_id}")
        return {
            "task": rows
        }
