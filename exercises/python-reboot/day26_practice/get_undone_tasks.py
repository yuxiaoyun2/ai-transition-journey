tasks = [
    {"title": "buy milk", "done": False},
    {"title": "study python", "done": True},
    {"title": "write code", "done": False},
]

def get_undone_tasks(tasks):
    return [task for task in tasks if not task.get("done", False)]

def get_undone_tasks_by_filter(tasks):
    return list(filter(lambda task: not task["done"]), tasks)

tasks = [
    {"title": "task1", "priority": "low"},
    {"title": "task2", "priority": "high"},
    {"title": "task3", "priority": "medium"},
]
def sort_by_priority(tasks):
    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2
    }
    return sorted(tasks, key=lambda task: priority_order[task["priority"]])


def get_valid_priority():
    valid_priority = ["high","medium", "low"]
    
    while True:
        value = input("input a value in ['high','medium', 'low']: ").strip().lower()
        
        if value in valid_priority:
            return value
        
        print("invalid value, please input again")