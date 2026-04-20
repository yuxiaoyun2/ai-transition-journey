import sys
from todo_manager import TodoManager

manager = TodoManager()

if len(sys.argv) < 2:
    print("please input command: add/ list")
    exit()
    
command = sys.argv[1]

if command == "add":
    title = sys.argv[2]
    manager.add_task(title)
    print("已添加")
    
elif command == "list":
    tasks = manager.list_tasks()
    for i, t in enumerate(tasks):
        print(f"{i+1}. {t.display()}")