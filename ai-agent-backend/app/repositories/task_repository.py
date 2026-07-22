from sqlalchemy.orm import Session
from app.models.task import Task


class TaskRepository:

    def __init__(self, db: Session):
        self.db = db
        self.model = Task

    def create(self, title: str) -> Task:
        task = Task(title=title)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_tasks(self) -> list[Task]:
        return self.db.query(self.model).all()

    def get_task(self, _task_id: int) -> Task | None:
        return self.db.get(self.model, _task_id)

    def delete_task(self, task_id: int) -> bool:
        task = self.db.get(self.model, task_id)
        if task is None:
            return False

        self.db.delete(task)
        self.db.commit()

        return True
