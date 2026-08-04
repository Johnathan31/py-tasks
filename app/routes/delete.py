from typing import Optional
from .router import router
from ..internal.types import Conn
from ..internal.models import TaskIds
from fastapi import HTTPException

# DELETE /v2/tasks/


@router.delete("/", tags=["Delete"], status_code=204)
def delete_all(
    connection: Conn,
    body: Optional[TaskIds] = None
):
    with connection.cursor() as cursor:
        if not body:  # type: ignore
            cursor.execute("DELETE FROM tasks;")
        else:
            ids: list[int] = list(set(body.ids))

            if not ids:
                raise HTTPException(
                    status_code=422,
                    detail={
                        "error": "No provided task IDs."
                    }
                )
            clause = " OR ".join(
                "id = %s"
                for _ in ids
            )

            query: str = f"""
                DELETE FROM tasks
                WHERE {clause}
                RETURNING id;
            """

            cursor.execute(
                query,
                ids
            )

            deleted_ids: list = cursor.fetchall()

        if body:
            if len(deleted_ids) != len(ids):  # type: ignore
                raise HTTPException(
                    status_code=404,
                    detail={
                        "error": "Some task IDs were not found.",

                        # type: ignore
                        "found_ids": [row["id"] for row in deleted_ids]
                    }
                )

        return


# DELETE /v2/tasks/{_id}
@router.delete("/{_id:int}", tags=["Delete"], status_code=204)
def delete_task_by_id(_id: int, connection: Conn):
    with connection.cursor() as cursor:

        cursor.execute(
            """
            DELETE FROM tasks
            WHERE id = %s;
            """,
            [_id]
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                404,
                detail={
                    "error": f"No task with ID {_id}"
                }
            )

        return


# DELETE /v2/tasks/completed
@router.delete("/completed", tags=["Delete"], status_code=204)
def delete_done_tasks(connection: Conn):
    with connection.cursor() as cursor:
        cursor.execute(
            """
                DELETE FROM tasks
                WHERE done = TRUE;
                """
        )

        return
