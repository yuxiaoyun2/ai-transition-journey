## Day18 总结

### 1️⃣ 今天学了什么

* edit 功能实现（修改任务标题）
* 输入校验逻辑抽离（update_title）
* CLI 异常处理（try / except）
* CLI 输出结构优化（分组 + 排版）
* 展示逻辑抽离（print_grouped_tasks）
* pytest CLI 测试（sys.argv / capsys）
* pytest 执行路径问题解决

---

### 2️⃣ 核心代码

```python
def edit_task(self, index: int, new_title: str):
    for task in self.tasks:
        if task.index == index:
            task.title = self.update_title(task.title, new_title)
            return task
    raise ValueError("任务不存在")
```

```python
def update_title(self, old_title: str, new_title: str):
    new_title = new_title.strip()

    if not new_title:
        raise ValueError("标题不能为空")

    if new_title == old_title.strip():
        return old_title

    return new_title
```

```python
def handle_edit(manager, args):
    try:
        task = manager.edit_task(index=args.index - 1, new_title=args.title)
        print("タスクを更新しました")
        print(task.display())
    except ValueError as e:
        print(e)
```

---

### 3️⃣ 我理解的本质（最重要❗）

* CLI 不只是命令执行，而是“用户界面”
* 业务逻辑 和 输入输出 应该分层
* 错误处理应该用 Exception，而不是 if 判断
* 重复逻辑应该抽象成函数（update_title）

👉 核心思想：

输入 → 清洗 → 校验 → 业务处理 → 输出


---

### 4️⃣ 我踩的坑

* argparse 参数名不一致（title vs new_title）
* type="str" 写错
* sys.args 写错，应为 sys.argv
* CLI 没有 try/except 导致程序崩溃
* edit 前没有 add（测试失败）
* pytest 找不到模块（执行路径问题）
* 输出格式换行错误
* 忘记复用 update_title（重复逻辑）

---

### 5️⃣ 明天要做什么

* edit 支持部分更新（--title / --priority）
* CLI 参数设计优化（optional 参数）
* 参数组合逻辑处理
* 提升 CLI 使用体验（更接近真实工具）

---

### Day18 一句话总结

👉 CLI 不是 print，而是产品界面