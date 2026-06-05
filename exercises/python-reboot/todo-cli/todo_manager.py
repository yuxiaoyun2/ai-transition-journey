from task import Task
from typing import List
import json
import os
import logging

logging.basicConfig(
    filename="todo.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    encoding="utf-8",
)

logger = logging.getLogger(__name__)


class TodoManager:
    def __init__(self, file_path: str = "todo.json"):
        self.file_path = file_path
        self.tasks: List[Task] = []
        self.load_tasks()

    def add_task(self, title, priority="medium"):
        index = len(self.tasks)
        task = Task(index=index, title=title, priority=priority)
        self.tasks.append(task)
        self.save_tasks()
        logger.info(f"task added: {task.title}")
        logger.debug("debug message")

    def get_tasks(
        self,
        undone: bool = False,
        done: bool = False,
        keyword=None,
        priority=None,
        sort=None,
    ):
        tasks = self.tasks
        if priority:
            tasks = filter(lambda task: task.priority == priority, tasks)

        if undone:
            tasks = filter(lambda task: not task.done, tasks)

        elif done:
            tasks = filter(lambda task: task.done, tasks)

        if keyword:
            tasks = filter(lambda task: keyword.lower() in task.title.lower(), tasks)

        if sort == "asc":
            tasks = sorted(tasks, key=lambda task: task.index)

        elif sort == "desc":
            tasks = sorted(tasks, key=lambda task: task.index, reverse=True)

        elif sort == "priority":
            priority_order = {"high": 3, "medium": 2, "low": 1}
            tasks = sorted(
                tasks,
                key=lambda task: (-priority_order.get(task.priority, 0), task.index),
            )

        elif sort == "smart":
            priority_order = {"high": 3, "medium": 2, "low": 1}
            tasks = sorted(
                tasks,
                key=lambda task: (
                    task.done,
                    -priority_order.get(task.priority, 0),
                    task.index,
                ),
            )

        return list(tasks)

    def mark_done(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks[index].done = True
            self.save_tasks()
            logger.info(f"task done: {self.tasks[index].title}")
            return self.tasks[index]

        logger.error(f"mark_done failed: index={index}")
        raise ValueError("task not found")

    def remove_task_by_index(self, index: int):
        if 0 <= index < len(self.tasks):
            task = self.tasks.pop(index)
            self.reindex_tasks()
            self.save_tasks()
            logger.info(f"task deleted: {task.title}")
            return task

        logger.error(f"remove_task failed: index={index}")
        raise ValueError("task not found")

    def total_list(self) -> int:
        return len(self.tasks)

    def load_tasks(self):
        if not os.path.exists(self.file_path):
            self.tasks = []
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ JSONファイルが破損していたため、空のリストにリセットしました。")
            self.tasks = []
            return

        tasks = []
        for i, item in enumerate(data):
            try:
                task = Task.from_dict(item, index=i)
                tasks.append(task)
            except ValueError as e:
                print(f"不正なデータをスキップしました: {item}, ({e})")
        self.tasks = tasks
        self.reindex_tasks()
        self.save_tasks()

    def save_tasks(self):
        data = [task.to_dict() for task in self.tasks]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def reindex_tasks(self):
        for i, task in enumerate(self.tasks):
            task.index = i

    def edit_task(self, index: int, title: str = None, priority: str = None):
        for task in self.tasks:
            if task.index == index:
                if title is not None:
                    task.title = self.update_title(task.title, title)
                if priority is not None:
                    task.priority = self.update_priority(task.priority, priority)
                self.save_tasks()
                return task

        raise ValueError("その番号のタスクはありません")

    def update_title(self, old_title: str, new_title: str):
        new_title = new_title.strip()
        if not new_title:
            raise ValueError("タイトルは必須です。")

        if new_title == old_title.strip():
            return old_title

        return new_title

    def update_priority(self, old_priority: str = None, new_priority: str = None):
        if not new_priority or new_priority == old_priority:
            return old_priority

        if new_priority not in ["high", "medium", "low"]:
            raise ValueError(
                "優先度は「high」「medium」「low」のいずれかでなければなりません。"
            )

        return new_priority

    def get_task_by_index(self, index: int):
        for task in self.tasks:
            if task.index == index:
                return task
        return None
