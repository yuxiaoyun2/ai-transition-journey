import argparse
from todo_manager import TodoManager


def main():
    manager = TodoManager()

    parser = argparse.ArgumentParser(description="Simple Todo CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task title")

    subparsers.add_parser("list", help="List all tasks")

    done_parser = subparsers.add_parser("done", help="Mark task as done")
    done_parser.add_argument("index", type=int, help="Task index")

    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("index", type=int, help="Task index")

    args = parser.parse_args()

    if args.command == "add":
        manager.add_task(args.title)
        print("タスクを追加しました")

    elif args.command == "list":
        tasks = manager.list_tasks()
        if not tasks:
            print("タスクはありません")
        else:
            for task in tasks:
                print(task.display())

    elif args.command == "done":
        success = manager.task_done(args.index - 1)
        if success:
            print("タスクを完了しました")
        else:
            print("その index のタスクはありません")

    elif args.command == "remove":
        success = manager.remove_task_by_index(args.index - 1)
        if success:
            print("タスクを削除しました")
        else:
            print("その index のタスクはありません")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()