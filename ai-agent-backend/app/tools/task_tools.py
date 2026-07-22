from datetime import datetime

from agents import function_tool

from app.repositories.task_repository import TaskRepository

from app.database import SessionLocal

import logging

logger = logging.getLogger(__name__)


@function_tool
def get_current_datetime() -> str:
    """Return the current server date and time."""

    current_datetime = datetime.now()

    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")


@function_tool
def create_task(title: str) -> dict:
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

        result = {
            "id": task.id,
            "title": task.title,
            "create_at": task.created_at.isoformat(),
        }

        logger.info("Task created successfully: %s", result)
        return result

    except Exception as e:
        db.rollback()
        logger.exception("failed to create task: %s", e)
        raise

    finally:
        db.close()


@function_tool
def get_tasks() -> list[dict]:
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

        result = [
            {
                "id": task.id,
                "title": task.title,
            }
            for task in tasks
        ]
        logger.info("Tasks get successfully: %s", result)
        return result

    except Exception as e:
        logger.exception("failed to get tasks: %s", e)
        raise

    finally:
        db.close()


@function_tool
def get_task_by_id(task_id: int) -> dict:
    """
    Retrieve a task by ID.

    Args:
        id (int): the task ID

    Returns:
        dict: return information or a not-found result.
    """
    db = SessionLocal()
    try:
        repository = TaskRepository(db)
        task = repository.get_task(task_id)

        if task is None:
            return {"success": False, "message": f"Task {task_id} was not found."}

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
            },
        }

    except Exception:
        logger.exception("failed to get task_id= %s", task_id)
        raise

    finally:
        db.close()


@function_tool
def delete_task(task_id: int) -> dict:
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
            return {
                "success": False,
                "message": f"Task {task_id} was not found.",
            }

        return {
            "success": True,
            "message": f"Task {task_id} was deleted.",
        }

    except Exception:
        db.rollback()
        logger.exception("failed to delete task: task_id = %s", task_id)
        raise

    finally:
        db.close()


@function_tool
def search_tasks(keyword: str) -> list[dict]:
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

        result = [
            {
                "id": task.id,
                "title": task.title,
            }
            for task in tasks
        ]
        logger.info(
            "Tasks searched successfully: keyword = %s, count = %s",
            keyword,
            len(tasks),
        )
        return result

    except Exception:
        logger.exception("failed to search tasks: keyword = %s", keyword)
        raise

    finally:
        db.close()


@function_tool
def update_task(task_id: int, title: str) -> dict:
    """
    update task title by task ID.

    Args:
        task_id (int): task ID
        title (str): the new task title

    Returns:
        dict: The update result and updated Task information.
    """

    db = SessionLocal()
    try:
        repository = TaskRepository(db)
        task = repository.update_task(task_id, title)

        if task is None:
            return {
                "success": False,
                "message": f"Task {task_id} was not found.",
            }

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
            },
        }

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
