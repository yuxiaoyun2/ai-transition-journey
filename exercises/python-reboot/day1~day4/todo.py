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
    add_parser.add_argument("--title", type=str, help="Task title")
    add_parser.add_argument("--priority", choices=["high","medium","low"],default="medium")

    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--priority", choices=["high","medium","low"])
    list_parser.add_argument("--undone", action="store_true")
    list_parser.add_argument("--sort", choices=["asc", "desc", "priority", "smart"])
    list_parser.add_argument("--done", action="store_true")
    list_parser.add_argument("--keyword", type=str)

    done_parser = subparsers.add_parser("done", help="Mark task as done")
    done_parser.add_argument("index", type=int, help="Task index")

    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("index", type=int, help="Task index")
    
    edit_parser = subparsers.add_parser("edit", help="Edit a task")
    edit_parser.add_argument("index", type=int, help="Task index")
    edit_parser.add_argument("--title", type=str, help="Task new title")
    edit_parser.add_argument("--priority", type=str, choices=["high","medium","low"], help="Task priority")
    
    return parser
    
def handle_list(manager, args):
    if args.done and args.undone:
        print("--done と --undone は同時に指定できません") 
        return
    filtered_tasks = manager.get_tasks(priority=args.priority, undone=args.undone, done=args.done, sort=args.sort, keyword=args.keyword)  
    if not filtered_tasks:
        if args.priority or args.keyword:
            print("条件に一致するタスクはありません")
        elif args.undone:
            print("未完了のタスクはありません") 
        elif args.done:
            print("完了したタスクはありません")
        else:
            print("タスクはありません")
        return
    print_grouped_tasks(filtered_tasks)
    
    while True:
        action = prompt_action()
        if action in  ["1","2","3"]:
            break
    
    if action == "1":
        index = get_valid_index(len(filtered_tasks))
        task = filtered_tasks[index]
        manager.mark_done(task.index)
        print(f"任务已标记完成: {task.title}\n")
        
    elif action == "2":
        index = get_valid_index(len(filtered_tasks))
        task = filtered_tasks[index]
        manager.remove_task_by_index(task.index)
        print(f"任务已删除: {task.title}\n")
        
    elif action == "3":
        print("退出操作")
        return
        
def prompt_action():
    print("\n👉 请选择操作:")
    print("1. 标记完成")
    print("2. 删除任务")
    print("3. 退出")
    
    return input("输入选项: ").strip()

     
    
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
    if args.title:
        title = args.title
            
    else:
        while True:
            title = input("请输入任务标题: ").strip()
            if title != "":
                break
            else:
                print("标题不能为空")
            
    priority = get_valid_input("优先级", ["high", "medium", "low"])
        
    manager.add_task(title = title, priority= priority)
    print("タスクを追加しました")

def handle_edit(manager, args):
    try:
        if args.title is None and args.priority is None:
            handle_edit_interactive(manager,args)
        else:
            task = manager.edit_task(index = args.index-1, title = args.title, priority = args.priority)
            print("タスクを更新しました")
            print(task.display())
    except ValueError as e:
        print(e)
    
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
            
    elif args.command == "edit":
        handle_edit(manager, args)
    else:
        parser.print_help()
    

def print_grouped_tasks(tasks:list[Task]):
    undone_task = [task for task in tasks if not task.done]
    done_task = [task for task in tasks if task.done]
        
    if undone_task:
        print(f"[未完了]({len(undone_task)})")
        print_tasks(undone_task)
    if done_task:
        print(f"\n[完了]({len(done_task)})") 
        print_tasks(done_task)
    print(f"\n合計: {len(tasks)}")

def handle_edit_interactive(manager, args):
    task = manager.get_task_by_index(args.index - 1)
    
    if not task:
        print("任务不存在")
        return
        
    print(f"当前标题: {task.title}")
    new_title = input("新标题（回车跳过）: ")
    
    print(f"当前优先级: {task.priority}")
    new_priority = input("新优先级（high/medium/low，回车跳过）: ")
    
    title = new_title.strip() if new_title.strip() else None
    priority = new_priority.strip() if new_priority.strip() else None
    
    if title is None and priority is None:
        raise ValueError("没有修改任何内容")
    
    task = manager.edit_task(index = args.index -1, title = title, priority = priority)
    
    print("タスクを更新しました")
    print(task.display())

def get_valid_input(prompt: str, valid_options: list[str]) -> str:
    while True:
        value = input(f"{prompt}({'/'.join(valid_options)}): ").strip().lower()
        
        if value in valid_options:
            return value
        
        print("输入有误，请重新输入")
        
def get_valid_index(max_index: int) -> int:
    while True:
        value = input(f"请输入任务编号 (1 ~ {max_index}): ").strip()
        
        if not value.isdigit():
            print("❌ 必须输入数字")
            continue
        
        index = int(value)
        
        if 0<index <= max_index:
            return index-1
        
        print("❌ 编号超出范围")  

if __name__ == "__main__":
    main()