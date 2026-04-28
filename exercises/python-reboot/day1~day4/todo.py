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

    try:
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
            manager.task_done(args.index - 1)
            print("タスクを完了しました")     

        elif args.command == "remove":
            manager.remove_task_by_index(args.index - 1)
            print("タスクを削除しました")

        else:
            parser.print_help()
            
    except ValueError:
        print("その index のタスクはありません")
    

if __name__ == "__main__":
    main()