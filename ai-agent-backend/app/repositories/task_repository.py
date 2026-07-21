class TaskRepository:

    def __init__(self):
        self.tasks = []

    def create_task(self, title: str) -> str:
        self.tasks.append(title)
        return title

    def get_tasks(self) -> list[str]:
        return self.tasks
