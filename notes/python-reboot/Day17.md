## Day17 总结

### day17复习
将 CLI 输出从“纯数据打印”升级为“结构化展示”

### 1️⃣ 今天学了什么

* 任务分组展示（未完了 / 完了）
* CLI 输出结构优化（标题 + 空行 + 排版）
* 输出信息增强（数量统计 + 合计）
* 逻辑与展示分离（handle_list / print_grouped_tasks）
* pytest 输出捕获机制（capsys / -s）
* argparse 错误输出（stderr + SystemExit）
* Git 问题处理（目录 rename / 分支 / main 合并

---

### 2️⃣ 核心代码

```python
def print_grouped_tasks(tasks: list[Task]):
    undone_tasks = [task for task in tasks if not task.done]
    done_tasks = [task for task in tasks if task.done]

    if undone_tasks:
        print(f"[未完了] ({len(undone_tasks)})")
        print_tasks(undone_tasks)

    if done_tasks:
        print(f"\n[完了] ({len(done_tasks)})")
        print_tasks(done_tasks)

    print(f"\n合計: {len(tasks)}")
```

---

### 3️⃣ 我理解的本质（最重要❗）

* 输出不仅是 print，而是“用户界面”
* 数据 → 展示结构（分组 / 层级 / 间距）
* 业务逻辑 和 展示逻辑 应该分离
* CLI 也是产品的一种形式

👉 核心思想：
好输出 = 结构 + 信息 + 可读性

---

### 4️⃣ 我踩的坑

* sys.args 写错，应为 sys.argv
* pytest 默认捕获 print，看不到输出
* [完了] 输出格式错误
* 忘记 return 导致重复执行
* 改文件夹导致 Git 路径混乱
* GitHub contribution 没有 merge 到 main

---

### 5️⃣ 明天要做什么

进入“真实 CLI 行为设计”：

* 参数组合逻辑（--done / --undone / --priority）
* 输出自动适配（只显示相关分组）
* CLI 使用体验优化（更像真实工具）
* 错误提示优化

---

### Day16 一句话总结

👉 CLI 输出就是产品界面