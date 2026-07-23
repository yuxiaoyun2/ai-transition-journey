from pydantic import BaseModel, Field


class TaskItem(BaseModel):
    id: int
    title: str


class TaskResponse(BaseModel):
    success: bool
    message: str
    task: TaskItem | None = None


class TaskListResponse(BaseModel):
    success: bool
    message: str
    tasks: list[TaskItem] = Field(default_factory=list)
