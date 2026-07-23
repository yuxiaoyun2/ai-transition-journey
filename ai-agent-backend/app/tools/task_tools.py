from datetime import datetime

from agents import function_tool

from app.repositories.task_repository import TaskRepository

from app.database import SessionLocal

from app.schemas.task_schema import TaskResponse, TaskItem, TaskListResponse

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

        logger.info("Task created successfully: %s", result)
        return result

    except Exception as e:
        db.rollback()
        logger.exception("failed to create task: %s", e)
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
        logger.info("Tasks retrieved successfully: %s", result)
        return result

    except Exception as e:
        logger.exception("failed to get tasks: %s", e)
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
        dict: return information or a not-found result.
    """
    db = SessionLocal()
    try:
        repository = TaskRepository(db)
        task = repository.get_task(task_id)

        if task is None:
            return TaskResponse(
                success=False,
                message=f"Task {task_id} was not found.",
            )

        return TaskResponse(
            success=True,
            message="Task retrieved successfully.",
            task=TaskItem(
                id=task.id,
                title=task.title,
            ),
        )

    except Exception:
        logger.exception("failed to get task_id= %s", task_id)
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

        deleted = repository.delete_task(task_id)

        if not deleted:
            return TaskResponse(
                success=False,
                message=f"Task {task_id} was not found.",
            )

        return TaskResponse(
            success=True,
            message=f"Task {task_id} was deleted.",
        )

    except Exception:
        db.rollback()
        logger.exception("failed to delete task: task_id = %s", task_id)
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
        logger.exception("failed to search tasks: keyword = %s", keyword)
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
        dict: The update result and updated Task information.
    """

    db = SessionLocal()
    try:
        repository = TaskRepository(db)
        task = repository.update_task(task_id, title)

        if task is None:
            return TaskResponse(
                success=False,
                message=f"Task {task_id} was not found.",
            )

        return TaskResponse(
            success=True,
            message="Task updated successfully.",
            task=TaskItem(
                id=task.id,
                title=task.title,
            ),
        )

    except Exception:
        db.rollback()
        logger.exception(
            "failed to update task: task_id = %s, title = %s ",
            task_id,
            title,
        )
        raise

    finally:
        db.close()
