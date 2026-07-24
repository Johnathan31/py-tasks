from fastapi import APIRouter

router: APIRouter = APIRouter(
    prefix="/tasks",
    tags=["CRUD"]
)
