from typing import Any
from ..internal.types import Conn
from .router import router
from ..internal.models import TaskFields, TaskOptionalFields
from fastapi import HTTPException

# PUT /tasks/{_id}


@router.put(
    "/{_id:int}",
    tags=["Update"],
    status_code=204
)
def update_task_by_id(
    _id: int,
    body: TaskFields,
    connection: Conn
):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE tasks
            SET title = %s,
                priority = %s,
                done = %s
            WHERE id = %s;
            """,
            [
                body.title,
                body.priority,
                body.done,
                _id
            ]
        )
        if cursor.rowcount == 0:
            raise HTTPException(
                404,
                detail=F"No task with ID {_id}"
            )

        return


# PATCH /tasks/{_id}
@router.patch(
    "/{_id:int}",
    tags=["Update"],
    status_code=204
)
def update_task_field(
    connection: Conn,
    _id: int,
    body: TaskOptionalFields
):
    with connection.cursor() as cursor:
        updates: dict[str, Any] = body.model_dump(exclude_unset=True)
        if not updates:
            raise HTTPException(
                400,
                detail="No field(s) to update."
            )

        cursor.execute(
            """
            SELECT * FROM tasks
            WHERE id = %s;
            """,
            [_id]
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                404,
                detail=f"No task found with id {_id}"
            )

        clause = ", ".join(
            f"{field} = %s"
            for field in updates
        )

        values = list(updates.values())
        values.append(_id)

        query: str = f"""
        UPDATE tasks
        SET {clause}
        WHERE id = %s
        """

        cursor.execute(query, values)  # type: ignore

        return
