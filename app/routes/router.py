from fastapi import APIRouter

router: APIRouter = APIRouter(
    prefix="/v3/tasks",
    tags=["CRUD"]
)
