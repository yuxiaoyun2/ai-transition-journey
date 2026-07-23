from sqlalchemy.orm import Session
from app.models.task import Task
from app.exceptions.task_exceptions import (
    TaskNotFoundError,
    TaskTitleEmptyError,
    TaskAlreadyExistsError,
)


class TaskRepository:

    def __init__(self, db: Session):
        self.db = db
        self.model = Task

    def create(self, title: str) -> Task:
        clean_title = title

        if not clean_title:
            raise TaskTitleEmptyError()

        existing_task = (
            self.db.query(self.model).filter(self.model.title == clean_title).first()
        )
        if existing_task is not None:
            raise TaskAlreadyExistsError(f"Task {clean_title} already exists.")

        task = Task(title=clean_title)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return task

    def get_tasks(self) -> list[Task]:
        return self.db.query(self.model).all()

    def get_task(self, task_id: int) -> Task:
        task = self.db.get(self.model, task_id)

        if task is None:
            raise TaskNotFoundError(f"Task {task_id} was not found.")

        return task

    def delete_task(self, task_id: int) -> None:
        task = self.db.get(self.model, task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} was not found")

        self.db.delete(task)
        self.db.commit()

    def search_tasks(self, keyword: str) -> list[Task]:
        clean_keyword = keyword.strip()

        if not clean_keyword:
            return []

        return (
            self.db.query(self.model)
            .filter(self.model.title.contains(clean_keyword))
            .all()
        )

    def update_task(self, task_id: int, title: str) -> Task:
        clean_title = title.strip()

        if not clean_title:
            raise TaskTitleEmptyError()

        task = self.db.get(self.model, task_id)

        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found.")

        task.title = clean_title

        self.db.commit()
        self.db.refresh(task)

        return task
