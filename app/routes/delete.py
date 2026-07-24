from typing import Optional
from .router import router
from ..internal.types import Conn
from ..internal.models import TaskIds
from fastapi import HTTPException

# DELETE /tasks/


@router.delete("/", tags=["Delete"], status_code=204)
def delete_all(
    connection: Conn,
    body: Optional[TaskIds] = None
):
    with connection.cursor() as cursor:
        if not body:  # type: ignore
            cursor.execute("DELETE FROM tasks;")
        else:
            if len(body.ids) < 1:
                raise HTTPException(
                    status_code=422,
                    detail={
                        "error": "No provided task IDs."
                    }
                )
            clause = " OR ".join(
                "id = %s"
                for _ in body.ids  # type: ignore
            )

            query: str = f"""
                    DELETE FROM tasks
                    WHERE {clause}
                    RETURNING id;
                    """

            cursor.execute(
                query,
                body.ids
            )

            deleted_ids: list = cursor.fetchall()

        if not body:

            if cursor.rowcount < 0:
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "internal server error.",
                    }
                )
        else:
            if len(deleted_ids) != len(body.ids):  # type: ignore
                raise HTTPException(
                    status_code=404,
                    detail={
                        "error": "Some task IDs were not found.",

                        # type: ignore
                        "deleted_ids": [row[0] for row in deleted_ids]
                    }
                )

        return


# DELETE /tasks/{_id}
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
                detail=f"No task with ID {_id}"
            )

        return


# DELETE /tasks/completed
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
