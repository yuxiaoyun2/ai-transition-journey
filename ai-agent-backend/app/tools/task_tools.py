from datetime import datetime
from agents import function_tool

from app.repositories.task_repository import TaskRepository
from app.database import SessionLocal
from app.schemas.task_schema import TaskResponse, TaskItem, TaskListResponse
from app.exceptions.task_exceptions import (
    TaskNotFoundError,
    TaskTitleEmptyError,
    TaskAlreadyExistsError,
)

import logging

logger = logging.getLogger(__name__)


@function_tool
def get_current_datetime() -> str:
    """Return the current server date and time."""

    current_datetime = datetime.now()

    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")


@function_tool
def create_task(title: str) -> TaskResponse:
    """
    Create a new task.

    Args:
        title: Task title.

    Returns:
        Created task information.
    """
    db = SessionLocal()
    logger.info("create_task tool was called: title=%s", title)
    try:
        repository = TaskRepository(db)
        task = repository.create(title=title)

        result = TaskResponse(
            success=True,
            message="Task created successfully.",
            task=TaskItem(
                id=task.id,
                title=task.title,
            ),
        )

        logger.info(
            "Task created successfully: %s",
            result,
        )
        return result

    except (TaskTitleEmptyError, TaskAlreadyExistsError) as exc:
        db.rollback()
        logger.warning(
            "Task created failed: %s",
            exc,
        )
        return TaskResponse(
            success=False,
            message=str(exc),
        )

    except Exception:
        db.rollback()
        logger.exception(
            "Unexpected error while creating task: task_title = %s",
            title,
        )
        raise

    finally:
        db.close()


@function_tool
def get_tasks() -> TaskListResponse:
    """
    Get all tasks.

    Returns:
        A list of task information.
    """
    db = SessionLocal()
    logger.info("get_tasks tool was called")
    try:
        repository = TaskRepository(db)
        tasks = repository.get_tasks()

        task_items = [
            TaskItem(
                id=task.id,
                title=task.title,
            )
            for task in tasks
        ]
        result = TaskListResponse(
            success=True,
            message="Tasks retrieved successfully.",
            tasks=task_items,
        )
        logger.info(
            "Tasks retrieved successfully: %s",
            result,
        )
        return result

    except Exception:
        logger.exception("Unexpected error while getting task list")
        raise

    finally:
        db.close()


@function_tool
def get_task_by_id(task_id: int) -> TaskResponse:
    """
    Retrieve a task by ID.

    Args:
        task_id: the task ID

    Returns:
        TaskResponse: The task information or a not-found result.
    """
    db = SessionLocal()
    try:
        repository = TaskRepository(db)
        task = repository.get_task(task_id)

        return TaskResponse(
            success=True,
            message="Task retrieved successfully.",
            task=TaskItem(
                id=task.id,
                title=task.title,
            ),
        )
    except TaskNotFoundError as exc:
        logger.warning(
            "Task was not found: task_id=%s",
            task_id,
        )
        return TaskResponse(
            success=False,
            message=str(exc),
        )

    except Exception:
        logger.exception(
            "Unexpected error while getting task: task_id = %s",
            task_id,
        )
        raise

    finally:
        db.close()


@function_tool
def delete_task(task_id: int) -> TaskResponse:
    """delete a task by its ID.

    Args:
        task_id: the Task ID.

    Returns:
        The deletion result.
    """
    db = SessionLocal()
    try:
        repository = TaskRepository(db)
        repository.delete_task(task_id)

        return TaskResponse(
            success=True,
            message=f"Task {task_id} was deleted.",
        )

    except TaskNotFoundError as exc:
        logger.warning(
            "failed to delete task: task_id = %s",
            task_id,
        )

        return TaskResponse(
            success=False,
            message=str(exc),
        )

    except Exception:
        db.rollback()
        logger.exception(
            "Unexpected error while deleting task: task_id = %s",
            task_id,
        )
        raise

    finally:
        db.close()


@function_tool
def search_tasks(keyword: str) -> TaskListResponse:
    """
    search tasks by title keyword.

    Args:
        keyword: a keyword contained in the task title.

    Returns:
        a list of matching task information.
    """
    db = SessionLocal()
    try:
        repository = TaskRepository(db)
        tasks = repository.search_tasks(keyword)

        task_items = [
            TaskItem(
                id=task.id,
                title=task.title,
            )
            for task in tasks
        ]

        logger.info(
            "Tasks searched successfully: keyword = %s, count = %s",
            keyword,
            len(tasks),
        )
        return TaskListResponse(
            success=True,
            message="Task searched successfully.",
            tasks=task_items,
        )

    except Exception:
        logger.exception(
            "Unexpected error while updating task: keyword = %s",
            keyword,
        )
        raise

    finally:
        db.close()


@function_tool
def update_task(task_id: int, title: str) -> TaskResponse:
    """
    update task title by task ID.

    Args:
        task_id: task ID
        title: the new task title

    Returns:
        TaskResponse: The update result and updated Task information.
    """

    db = SessionLocal()
    try:
        repository = TaskRepository(db)
        task = repository.update_task(task_id, title)

        return TaskResponse(
            success=True,
            message="Task updated successfully.",
            task=TaskItem(
                id=task.id,
                title=task.title,
            ),
        )

    except (TaskTitleEmptyError, TaskNotFoundError) as exc:
        logger.warning(
            "failed to update task: task_id = %s, error = %s ",
            task_id,
            exc,
        )
        return TaskResponse(
            success=False,
            message=str(exc),
        )

    except Exception:
        db.rollback()
        logger.exception(
            "Unexpected error while updating task: task_id = %s",
            task_id,
        )
        raise

    finally:
        db.close()
