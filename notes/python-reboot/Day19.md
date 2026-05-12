## Day19 总结

### day19复习
为 Todo CLI 增加 edit 功能，并提升 CLI 工具的工程能力和用户体验

### 1️⃣ 今天学了什么

* edit 命令升级（支持部分更新）
* argparse 可选参数（--title / --priority）
* 多字段更新逻辑（optional 参数处理）
* 参数组合校验（至少更新一个字段）
* 复用校验函数（update_title / update_priority）
* CLI 接口设计（更接近真实工具）
* pytest 覆盖多种更新场景

---

### 2️⃣ 核心代码

```python
def edit_task(self, index: int, title: str = None, priority: str = None):
    if title is None and priority is None:
        raise ValueError("至少更新一个字段")

    for task in self.tasks:
        if task.index == index:
            if title is not None:
                task.title = self.update_title(task.title, title)

            if priority is not None:
                task.priority = self.update_priority(task.priority, priority)

            return task

    raise ValueError("任务不存在")
```

```python
def handle_edit(manager, args):
    try:
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

---

### 3️⃣ 我理解的本质（最重要❗）

⭐ 1. 接口设计（核心）
edit(index, title=None, priority=None)

👉 支持“部分更新”
👉 参数即能力

⭐ 2. 参数分类
index → 操作对象（必须）
title / priority → 修改内容（可选）

⭐ 3. Optional 参数处理模式
if xxx is not None:
    才更新

👉 避免误判空字符串

⭐ 4. 不要重复逻辑
update_title / update_priority 统一校验

👉 edit_task 只做“调度”

⭐ 5. CLI ≈ API
todo edit 1 --title "xxx"

≈

PATCH /tasks/1


---

### 4️⃣ 我踩的坑

❌ edit 命令参数顺序写错
❌ 忘记加 "edit"
❌ priority 值不合法（必须 high/medium/low）
❌ captured.out 写错
❌ readouterr 拼写错误
❌ 测试函数缩进错误
❌ 把参数写成位置参数而不是 --title / --priority
❌ 没处理“无参数更新”的情况

---

### 5️⃣ 明天要做什么

* 交互式 CLI（Interactive Mode）

---

### Day19 一句话总结

👉 从“写功能” → “设计接口”