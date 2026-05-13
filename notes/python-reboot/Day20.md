## Day20 总结

### day20复习
为 Todo CLI 增加 edit 功能，并提升 CLI 工具的工程能力和用户体验

### 1️⃣ 今天学了什么

* 交互式 CLI（input 输入）
* edit 命令支持交互模式（无参数时触发）
* CLI 模式判断（参数模式 vs 交互模式）
* 输入数据处理（strip + 空字符串 → None）
* 用户输入分支控制（是否更新字段）
* UI 输出与数据展示分离
* 手动测试交互功能（替代 pytest）

---

### 2️⃣ 核心代码

```python
def handle_edit(manager, args):
    try:
        # 无参数 → 进入交互模式
        if args.title is None and args.priority is None:
            handle_edit_interactive(manager, args)
            return

        task = manager.edit_task(
            index=args.index - 1,
            title=args.title,
            priority=args.priority
        )

        print("タスクを更新しました")
        print(task.display())

    except ValueError as e:
        print(e)
```

```python
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
        print("没有修改任何内容")
        return

    task = manager.edit_task(
        index=args.index - 1,
        title=title,
        priority=priority
    )

    print("タスクを更新しました")
    print(task.display())
```

---

### 3️⃣ 我理解的本质（最重要❗）

⭐ 1. CLI 是“应用程序”，不是脚本
命令输入 → 用户交互 → 状态反馈 → 输出结果
⭐ 2. 双模式设计（关键）
参数模式：todo edit 1 --title xxx
交互模式：todo edit 1

👉 同一命令，不同使用方式

⭐ 3. 输入处理模式
input → strip → 空字符串 → None → 决策
⭐ 4. 用户体验设计（UX）
✔ 提示当前值
✔ 支持跳过（回车）
✔ 不强制输入
✔ 给出明确反馈
⭐ 5. 展示与逻辑分离
print("状态提示")
print(task.display())

👉 避免 UI 混乱

---

### 4️⃣ 我踩的坑

❌ 函数命名不一致（handling vs handle）
❌ edit_task 参数名写错（new_title / new_priority）
❌ 没处理“两个都回车”的情况
❌ UI 拼接错误（print 和 display 混用）
❌ JSON 手动修改导致数据异常
❌ 空 title 导致显示异常

---

### 5️⃣ 明天要做什么

体验优化（打磨产品感）

* 输入提示优化（显示当前值）
* 非法输入循环（让用户重新输入）
* 输出信息更自然（更像真实 CLI）
* 小重构（减少重复代码）

---

### Day20 一句话总结

👉 CLI 从“命令工具” → “可交互应用”