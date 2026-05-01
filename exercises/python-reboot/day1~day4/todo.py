import argparse
from todo_manager import TodoManager
from task import Task

def print_tasks(tasks: list[Task]):
    for task in tasks:
        print(task.display())

def main():
    manager = TodoManager()

    parser = argparse.ArgumentParser(description="Simple Todo CLI")
    subparsers = parser.add_subparsers(dest="command")
    

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task title")

    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--undone", action="store_true")
    list_parser.add_argument("--sort", choices=["asc", "desc"])
    list_parser.add_argument("--done", action="store_true")
    list_parser.add_argument("--keyword", type=str)

    done_parser = subparsers.add_parser("done", help="Mark task as done")
    done_parser.add_argument("index", type=int, help="Task index")

    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("index", type=int, help="Task index")
    
    args = parser.parse_args()

    if args.command == "add":
        manager.add_task(args.title)
        print("タスクを追加しました")

    elif args.command == "list":
        if args.done and args.undone:
            print("--done と --undone は同時に指定できません") 
            return
        tasks = manager.get_tasks(undone=args.undone, done=args.done, sort=args.sort, keyword=args.keyword)  
        if not tasks:
            if args.keyword:
                print("条件に一致するタスクはありません")
            elif args.undone:
                print("未完了のタスクはありません") 
            elif args.done:
                print("完了したタスクはありません")
            else:
                print("タスクはありません")
        else:
            print_tasks(tasks)

    elif args.command == "done":
        try:
            manager.task_done(args.index - 1)
            print("タスクを完了しました")
        except ValueError:
            print(f"その番号のタスクはありません: {args.index}")
        
    elif args.command == "remove":
        try:
            manager.remove_task_by_index(args.index - 1)
            print("タスクを削除しました")
        except ValueError:
            print(f"その番号のタスクはありません: {args.index}")
            
    else:
        parser.print_help()
    

if __name__ == "__main__":
    main()