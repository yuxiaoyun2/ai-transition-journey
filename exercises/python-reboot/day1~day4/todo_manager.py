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

    def get_tasks(self, undone: bool = False, done: bool = False, sort = None, keyword=None):
        tasks = self.tasks
        if undone:
            tasks = filter(lambda task: not task.done, tasks)
            
        elif done:
            tasks = filter(lambda task: task.done, tasks)
                    
        if keyword:
            tasks = filter(lambda task: keyword.lower() in task.title.lower(), tasks)
            
        if sort== "asc":
            tasks = sorted(tasks, key=lambda task: task.index)
            
        elif sort == "desc":
            tasks = sorted(tasks, key=lambda task: task.index, reverse=True)
        
        return list(tasks)
            
    def task_done(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks[index].done = True
            self.save_tasks()
            return self.tasks[index]
        
        raise ValueError("task not found")
                
                
    def remove_task_by_index(self, index: int):
        if 0 <= index < len(self.tasks):
            task = self.tasks.pop(index)
            self.reindex_tasks()
            self.save_tasks()
            return task
            
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
            print("⚠️ JSON 文件损坏，已重置为空列表")
            self.tasks = []
            return
            
        tasks = []
        for i, item in enumerate(data):
            try:
                task = Task.from_dict(item, index=i)
                tasks.append(task)
            except ValueError as e:
                print(f"跳过非法数据: {item}, ({e})")
        self.tasks = tasks
        self.reindex_tasks()
        self.save_tasks()
        
    def save_tasks(self):
        data = [task.to_dict() for task in self.tasks]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii= False, indent=2)
            
    def reindex_tasks(self):
        for i, task in enumerate(self.tasks):
            task.index = i
    
    # def list_tasks_sorted_by_index(self):
    #    return sorted(self.tasks, key=lambda task: task.index)
    
    # def list_tasks_sorted_desc(self):
    #     return sorted(self.tasks, key=lambda task: task.index, reverse= True)
    
    # def list_undone_tasks(self):
    #     return list(filter(lambda task: not task.done, self.tasks))
    
    # def list_undone_sorted(self):
    #     return sorted(filter(lambda task: not task.done, self.tasks ), key = lambda task: task.index)
    
    def get_done_tasks_sorted_desc(self):
        return sorted(filter(lambda task: task.done, self.tasks), key=lambda task:task.index, reverse= True)