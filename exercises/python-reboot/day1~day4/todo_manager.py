from task import Task
from typing import List
import json
import os
class TodoManager:
    def __init__(self, file_path: str = "todo.json"):
        self.file_path = file_path
        self.tasks: List[Task] = []
        self.load_tasks()
        
    def add_task(self, title):
        index = len(self.tasks)
        task = Task(index = index, title=title)
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        return self.tasks
            
    def task_done(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks[index].done = True
            self.save_tasks
            return self.tasks[index]
        
        raise ValueError("task not found")
                
                
    def remove_task_by_index(self, index: int):
        if 0 <= index < len(self.tasks):
            task = self.tasks.pop(index)
            self.save_tasks()
            return task
            
        raise ValueError("task not found")
        
    def total_list(self) -> int:
        return len(self.tasks)
    
    def load_tasks(self):
        if not os.path.exists(self.file_path):
            self.tasks = []
            return
        
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        self.tasks = [Task.from_dict(item, index=i) for i,item in enumerate(data)]
        
    def save_tasks(self):
        data = [task.to_dict() for task in self.tasks]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii= False, indent=2)
    