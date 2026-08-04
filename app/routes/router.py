from fastapi import APIRouter

router: APIRouter = APIRouter(
    prefix="/v1/tasks",
    tags=["CRUD"]
)
