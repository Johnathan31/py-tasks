from typing import Optional
from fastapi import HTTPException

from ..internal.models import Priorities
from ..internal.types import Conn
from .router import router

# GET /v2/tasks/


@router.get("/", tags=["Read"])
def view_tasks(
    connection: Conn,
    priority: Optional[Priorities] = None,
    done: Optional[bool] = None,
    search: Optional[str] = None
):
    with connection.cursor() as cursor:
        clauses: list[str] = []
        params: list = []

        if priority is not None:
            clauses.append("priority = %s")
            params.append(priority)

        if done is not None:
            clauses.append("done = %s")
            params.append(done)

        if search is not None:
            clauses.append("title ILIKE %s")
            params.append(f"%{search}%")

        query: str = f"""
        SELECT id,
               title,
               priority,
               done
        FROM tasks
        ORDER BY id
            """

        if clauses:
            query += f"\nWHERE " + " AND ".join(clauses) + ";"

        cursor.execute(query, params)  # type: ignore

        return {
            "tasks": cursor.fetchall()
        }


# GET /v2/tasks/{_id}
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
