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
