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
    add_parser.add_argument(
        "--priority", choices=["high", "medium", "low"], default="medium"
    )

    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--priority", choices=["high", "medium", "low"])
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
    edit_parser.add_argument(
        "--priority", type=str, choices=["high", "medium", "low"], help="Task priority"
    )

    return parser


def handle_list(manager, args):
    if args.done and args.undone:
        print("--done と --undone は同時に指定できません")
        return

    while True:
        filtered_tasks = filter_tasks(manager, args)

        if not filtered_tasks:
            print_empty_message(args)
            return

        print_grouped_tasks(filtered_tasks)
        action = prompt_action()

        if action == "1":
            task = select_task(filtered_tasks)
            manager.mark_done(task.index)
            print(f"タスクをマークしました: {task.title}\n")

        elif action == "2":
            task = select_task(filtered_tasks)
            manager.remove_task_by_index(task.index)
            print(f"タスクを削除しました: {task.title}\n")

        elif action == "3":
            print("操作退出")
            break
        else:
            print("入力が不正です。再入力してください。")


def select_task(tasks: list[Task]) -> Task:
    index = get_valid_index(len(tasks))
    return tasks[index]


def filter_tasks(manager, args):
    return manager.get_tasks(
        priority=args.priority,
        undone=args.undone,
        done=args.done,
        sort=args.sort,
        keyword=args.keyword,
    )


def print_empty_message(args):
    if args.priority or args.keyword:
        print("条件に一致するタスクはありません")
    elif args.undone:
        print("未完了のタスクはありません")
    elif args.done:
        print("完了したタスクはありません")
    else:
        print("タスクはありません")


def prompt_action():
    print("\n👉 操作を選択してください:")
    print("1. タスクをマークする")
    print("2. タスクを削除する")
    print("3. 退出")

    return input("操作番号を入力してください: ").strip()


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
            title = input("タスクのタイトルを入力してください: ").strip()
            if title != "":
                break
            else:
                print("タスクのタイトルは必須です")

    priority = get_valid_input("優先度", ["high", "medium", "low"])

    manager.add_task(title=title, priority=priority)
    print("タスクを追加しました")


def handle_edit(manager, args):
    try:
        if args.title is None and args.priority is None:
            handle_edit_interactive(manager, args)
        else:
            task = manager.edit_task(
                index=args.index - 1, title=args.title, priority=args.priority
            )
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


def print_grouped_tasks(tasks: list[Task]):
    undone_task = [task for task in tasks if not task.done]
    done_task = [task for task in tasks if task.done]

    if undone_task:
        print(f"===[未完了]({len(undone_task)})===")
        print_tasks(undone_task)
    if done_task:
        print(f"\n===[完了]({len(done_task)})===")
        print_tasks(done_task)
    print(f"\n合計: {len(tasks)}")


def handle_edit_interactive(manager, args):
    task = manager.get_task_by_index(args.index - 1)

    if not task:
        print("その番号のタスクはありません")
        return

    print(f"タスクのタイトル: {task.title}")
    new_title = input("新しいタイトル（Enterでスキップ）: ")

    print(f"現在の優先度: {task.priority}")
    new_priority = input("新しい優先度（high/medium/low，Enterでスキップ）: ")

    title = new_title.strip() if new_title.strip() else None
    priority = new_priority.strip() if new_priority.strip() else None

    if title is None and priority is None:
        raise ValueError("変更はありませんでした")

    task = manager.edit_task(index=args.index - 1, title=title, priority=priority)

    print("タスクを更新しました")
    print(task.display())


def get_valid_input(prompt: str, valid_options: list[str]) -> str:
    while True:
        value = input(f"{prompt}({'/'.join(valid_options)}): ").strip().lower()

        if value in valid_options:
            return value

        print("入力が不正です。再入力してください。")


def get_valid_index(max_index: int) -> int:
    while True:
        value = input(f"タスク番号を入力してください：(1 ~ {max_index}): ").strip()

        if not value.isdigit():
            print("❌ 数値を入力してください。")
            continue

        index = int(value)

        if 0 < index <= max_index:
            return index - 1

        print("❌ 番号が範囲を超えています。")


if __name__ == "__main__":
    main()
