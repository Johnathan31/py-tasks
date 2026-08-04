from fastapi import APIRouter

router: APIRouter = APIRouter(
    prefix="/v2/tasks/",
    tags=["CRUD"]
)
