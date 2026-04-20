from task import Task
from typing import List
class TodoManager:
    def __init__(self):
        self.tasks: List[Task] = []
        
    def add_task(self, title):
        index = len(self.tasks)
        task = Task(index = index, title=title)
        self.tasks.append(task)

    def list_tasks(self):
        return self.tasks
            
    def task_done(self, index: int):
        for task in self.tasks:
            if task.index == index:
                task.done = True
                
    def remove_task_by_index(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
        
    def total_list(self) -> int:
        return len(self.tasks)
    
    def load_tasks(self):
        return self.tasks
    
    def save_tasks(self, tasks):
        self.tasks = tasks
    