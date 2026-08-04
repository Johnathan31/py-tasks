from .router import router
from ..internal.models import TaskFields
from ..internal.types import Conn


# POST /v2/tasks/
@router.post("/", tags=["Create"], status_code=201)
def create_task(task: TaskFields, connection: Conn):
    with connection.cursor() as cursor:

        cursor.execute(
            """
                INSERT INTO tasks (title, priority, done)
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
            [task.title, task.priority, task.done]
        )

        return {"task": cursor.fetchone()}
