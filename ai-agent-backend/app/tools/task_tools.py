from datetime import datetime

from agents import function_tool

from app.repositories.task_repository import TaskRepository

repository = TaskRepository()


@function_tool
def get_current_datetime() -> str:
    """Return the current server date and time."""

    print("get_current_datetime tool was called")

    current_datetime = datetime.now()

    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")


@function_tool
def create_task(title: str) -> str:
    """Create a new task and return its title."""
    return repository.create_task(title=title)


@function_tool
def get_tasks() -> list[str]:
    """get tasks and return them."""
    return repository.get_tasks()
