import sys
from todo_manager import TodoManager

todo = TodoManager()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [add/list/done/delete]")
        return

    command = sys.argv[1]

    if command == "add":
        title = sys.argv[2]
        todo.add_task(title)

    elif command == "list":
        todo.list_tasks()

    elif command == "done":
        index = int(sys.argv[2])
        todo.mark_done(index)

    elif command == "delete":
        index = int(sys.argv[2])
        todo.delete_task(index)

    else:
        print("Unknown command")

if __name__ == "__main__":
    main()