import sys
from todo_manager import TodoManager

manager = TodoManager()

if len(sys.argv) < 2:
    print("please input command: add/ list")
    exit()
    
command = sys.argv[1]

if command == "add":
    if len(sys.argv) < 3:
        print("please input title")
        exit
    title = sys.argv[2]
    manager.add_task(title)
    print("已添加")
    
elif command == "list":
    tasks = manager.list_tasks()
    for i, t in enumerate(tasks):
        print(f"{i+1}. {t.display()}")