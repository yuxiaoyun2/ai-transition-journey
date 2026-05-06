import argparse
from todo_manager import TodoManager
from task import Task

def print_tasks(tasks: list[Task]):
    for task in tasks:
        print(task.display())

def create_parser():
    parser = argparse.ArgumentParser(description="Simple todo CLI")
    parser.add_argument("--file", default="todo.json")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True
    
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task title")
    add_parser.add_argument("--priority", choices=["high","medium","low"],default="medium")

    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--priority", choices=["high","medium","low"])
    list_parser.add_argument("--undone", action="store_true")
    list_parser.add_argument("--sort", choices=["asc", "desc", "priority"])
    list_parser.add_argument("--done", action="store_true")
    list_parser.add_argument("--keyword", type=str)

    done_parser = subparsers.add_parser("done", help="Mark task as done")
    done_parser.add_argument("index", type=int, help="Task index")

    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("index", type=int, help="Task index")
    
    return parser
    
def handle_list(manager, args):
    if args.done and args.undone:
        print("--done と --undone は同時に指定できません") 
        return
    tasks = manager.get_tasks(priority=args.priority, undone=args.undone, done=args.done, sort=args.sort, keyword=args.keyword)  
    if not tasks:
        if args.priority or args.keyword:
            print("条件に一致するタスクはありません")
        elif args.undone:
            print("未完了のタスクはありません") 
        elif args.done:
            print("完了したタスクはありません")
        else:
            print("タスクはありません")
    else:
        print_tasks(tasks) 
    
def handle_done(manager, args):
    try:
        manager.mark_done(args.index - 1)
        print("タスクを完了しました")
    except ValueError:
        print(f"その番号のタスクはありません: {args.index}")
        
def handle_remove(manager, args):
    try:
        manager.remove_task_by_index(args.index - 1)
        print("タスクを削除しました")
    except ValueError:
        print(f"その番号のタスクはありません: {args.index}")
            
def handle_add(manager, args):
    manager.add_task(args.title, priority = args.priority)
    print("タスクを追加しました")

def main():
    
    parser = create_parser()
    
    args = parser.parse_args()
    
    manager = TodoManager(file_path=args.file)

    if args.command == "add":
        handle_add(manager, args)

    elif args.command == "list":
        handle_list(manager, args)

    elif args.command == "done":
        handle_done(manager, args)
        
    elif args.command == "remove":
        handle_remove(manager, args)
            
    else:
        parser.print_help()
    

if __name__ == "__main__":
    main()