## Day22 总结

### day22 复习
将 CLI 控制流从“递归调用”升级为“循环驱动结构”

### 1️⃣ 今天学了什么

* 递归 → while 循环重构（控制流优化）
* CLI 主流程设计（展示 → 选择 → 操作 → 刷新）
* 状态驱动 UI（每次操作后重新获取 tasks）
* 公共逻辑抽取（filter_tasks）
* 空数据处理逻辑分离（print_empty_message）
* 数据流梳理（UI → task → index）
* 避免递归带来的结构复杂性

---

### 2️⃣ 核心代码

```python
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
            break

        else:
            print("无效选项，请重新输入")
```

---

### 3️⃣ 我理解的本质（最重要❗）

* CLI 不只是执行命令，而是一个“状态循环系统”
* 每次操作都应该基于最新数据（状态刷新）
* 控制流应该由循环统一管理，而不是函数互相调用
* 数据获取、展示、操作需要分层

👉 核心思想：
好结构 = 清晰控制流 + 明确数据流 + 单一职责

---

### 4️⃣ 我踩的坑

❌ 使用递归刷新 list（handle_list 调用自身）
❌ tasks 刷新逻辑依赖递归，而不是主动获取
❌ filter_tasks 中混入打印逻辑（职责不清）
❌ 空列表时仍然继续执行操作逻辑
❌ UI index 与 task.index 混用（Day21遗留问题）

---

### 5️⃣ 明天要做什么

进入“结构优化 + 工程化”：

* 用 Task 替代字符串
* done 用字段表示
* UI 根据字段显示
* 有 log_info / log_error
* 操作时有日志输出

---

### Day22 一句话总结

👉 CLI 的本质是“用户交互系统”，而不是“命令执行脚本”