## Day10 总结

### 1️⃣ 今天学了什么

* 代码重构（refactor）
* 函数职责拆分（Single Responsibility）
* CLI 结构优化（parser / handler 分离）
* 提高代码可读性和可维护性
* 为未来测试（test）做准备

---

### 2️⃣ 核心代码

```python
def create_parser():
    parser = argparse.ArgumentParser(description="Simple todo CLI")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True
    ...
    return parser
```

```python
def handle_list(manager, args):
    if args.done and args.undone:
        print("--done と --undone は同時に指定できません")
        return
    tasks = manager.get_tasks(...)
    ...
```

```python
def handle_done(manager, args):
    try:
        manager.task_done(args.index - 1)
    except ValueError:
        print(f"その番号のタスクはありません: {args.index}")
```

```python
def main():
    manager = TodoManager()
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "add":
        handle_add(manager, args)
    elif args.command == "list":
        handle_list(manager, args)
    elif args.command == "done":
        handle_done(manager, args)
    elif args.command == "remove":
        handle_remove(manager, args)
```

---

### 3️⃣ 我理解的本质（最重要❗）

* main() 不应该做太多事
* 每个函数只做一件事（Single Responsibility）
* CLI = 参数解析 + 命令分发
* handler = 具体业务逻辑

👉 核心结构：
```python
parser → args → handler → manager → output
```

---

### 4️⃣ 我踩的坑

* main() 过长（逻辑混在一起）
* CLI 参数定义和业务逻辑耦合
* 重复代码（print / try-except）
* handler 没拆前，可读性差

---

### 5️⃣ 明天要做什么

* 引入简单测试（pytest 基础）
* 测试 TodoManager（核心逻辑）
* 学会写可测试代码
* 进一步优化结构（依赖注入思维）

---

### Day10 一句话总结

👉 从“能跑的代码” → “结构清晰、可维护的代码”