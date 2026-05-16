## Day23 总结

### day23 复习
将 Todo 从“字符串处理”升级为“对象建模”，并引入日志系统

### 1️⃣ 今天学了什么

* 数据结构升级（list[str] → list[Task]）
* Task 类设计（title / done / priority）
* 状态管理方式变化（字符串标记 → 字段控制）
* UI 与数据分离（显示逻辑不再写入数据）
* 日志系统设计（log_info / log_error）
* log 分层（业务层 vs CLI 层）
* 异常与日志关系（log 在 raise 之前）

---

### 2️⃣ 核心代码

```python
class Task:
    def __init__(self, title: str):
        self.title = title
        self.done = False
```

```python
def task_list(tasks: list[Task]):
    for index, task in enumerate(tasks):
        status = "[x]" if task.done else "[ ]"
        print(f"{status} {index + 1}. {task.title}")
```

```python
def mark_done(self, index: int):
    if 0 <= index < len(self.tasks):
        task = self.tasks[index]
        task.done = True
        self.save_tasks()
        self.log_info(f"task done: {task.title}")
        return task

    self.log_error(f"mark_done failed: index={index}")
    raise ValueError("task not found")
```

---

### 3️⃣ 我理解的本质（最重要❗）

* 数据应该用结构化对象表示，而不是拼字符串
* UI 展示是“派生信息”，不应该写入数据本身
* log 是“系统行为记录”，不是用户输出
* 业务逻辑应该在 TodoManager 内部自洽（包含 log）

👉 核心思想：
好设计 = 数据结构清晰 + 表示与逻辑分离 + 行为可追踪

---

### 4️⃣ 我踩的坑

❌ 仍然尝试用字符串标记任务状态
❌ 忘记用 task.title，直接 print(task)
❌ mark_done 中变量作用域错误（task 未定义）
❌ log 写在 CLI 和 manager 两边（重复记录）
❌ log 写在 raise 之后（不会执行）
❌ log 字符串未使用 f-string（"{e}" 未展开）

---

### 5️⃣ 明天要做什么

进入“工程化升级”：

* 使用 Python logging 模块（替代 print log）
* 日志写入文件（而不是只打印）
* 日志等级（INFO / ERROR）
* 输出格式统一（CLI UI 优化）
* 项目结构整理（准备写 README）

---

### Day23 一句话总结

👉 数据用对象建模，行为用日志记录