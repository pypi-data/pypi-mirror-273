from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel

api = APIRouter()


class TasksCreateRequest(BaseModel):
    task: str


class TasksCreateResponse(BaseModel):
    id: UUID
    task: str


@api.post(
    "",
    status_code=201,
    response_model=TasksCreateResponse,
)
def create(request: TasksCreateRequest):
    return {
        "id": "e98d12c2-e50a-46d3-8cb8-9add8d426152",
        "task": request.task,
    }
