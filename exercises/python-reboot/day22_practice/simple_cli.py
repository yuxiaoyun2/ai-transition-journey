from task import Task


def get_valid_number(min_number: int, max_number: int):
    while True:
        value = input(f"请输入数字 ({min_number} ~ {max_number}: )").strip()
        if not value.isdigit():
            print("必须输入数字")
            continue

        number = int(value)

        if min_number <= number <= max_number:
            return number

        print("超出范围")


def select_item(items: list[str]):
    for index, item in enumerate(items):
        print(f"{index + 1}. {item}")
    selected_index = get_valid_number(1, len(items))
    return items[selected_index - 1]


def menu():
    while True:
        print("1. 打印 hello")
        print("2. 打印 world")
        print("3. 退出")

        selected_index = get_valid_number(1, 3)
        if selected_index == 1:
            print("hello")
        elif selected_index == 2:
            print("world")
        elif selected_index == 3:
            return


tasks = [Task("学习 Python"), Task("买奶粉"), Task("做饭")]


def run(tasks: list[Task]):

    while True:
        print("\n1. 查看任务")
        print("2. 标记完成")
        print("3. 删除任务")
        print("4. 退出")

        selected_number = get_valid_number(1, 4)

        if selected_number == 1:
            task_list(tasks)

        elif selected_number == 2:
            mark_done(tasks)

        elif selected_number == 3:
            delete_task(tasks)

        else:
            print("退出")
            return


def task_list(tasks: list[Task]):
    for index, task in enumerate(tasks):
        if task.done:
            print(f"[❌] {index + 1}. {task.title} \n")
        else:
            print(f"[ ] {index + 1}. {task.title} \n")


def mark_done(tasks: list[Task]):
    task_list(tasks)
    number = get_valid_number(1, len(tasks))
    index = number - 1
    task = tasks[index]

    if not task.done:
        task = tasks[index]
        task.done = True
        print(f"标记完成: {task.title}")
    else:
        print(f"已经是完成状态: {task.title}")


def delete_task(tasks: list[Task]):
    task_list(tasks)
    number = get_valid_number(1, len(tasks))
    index = number - 1
    task = tasks.pop(index)

    print(f"删除任务: {task.title}")


def main():
    run(tasks)


if __name__ == "__main__":
    main()
