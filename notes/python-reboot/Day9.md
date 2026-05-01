## Day9 总结

### 1️⃣ 今天学了什么

* CLI 用户体验优化（输出格式 / 提示信息）
* 参数校验（冲突检测）
* 错误处理升级（带上下文信息）
* 代码重构（函数拆分 print_tasks）
* 用户视角 vs 内部数据设计（index 1-based / 0-based）

---

### 2️⃣ 核心代码

```python
def display(self) -> str:
    status = "x" if self.done else " "
    return f"{self.index + 1}. [{status}] {self.title}"
```

```python
def print_tasks(tasks):
    for task in tasks:
        print(task.display())
```

```python
if args.done and args.undone:
    print("--done と --undone は同時に指定できません")
    return
```

```python
try:
    manager.task_done(args.index - 1)
except ValueError:
    print(f"その番号のタスクはありません: {args.index}")
```

---

### 3️⃣ 我理解的本质（最重要❗）

* CLI 工具不仅是“能跑”，还要“好用”
* 用户看到的 index ≠ 程序内部 index
* 错误提示要具体（带输入值）
* 参数必须校验（不能盲目执行）
* 重构 = 让代码更清晰，而不是变复杂

---

### 4️⃣ 我踩的坑

* 参数冲突没处理（--done + --undone）
* 错误提示太模糊（没有具体 index）
* main() 过长（职责不清）
* 重复代码（for print）
* 用户输入 index 和内部 index 混淆

---

### 5️⃣ 明天要做什么

* 拆分 main（函数职责划分）
* 抽出 parser 创建逻辑
* 代码结构优化（更像真实项目）
* 为测试做准备（可测试结构）
