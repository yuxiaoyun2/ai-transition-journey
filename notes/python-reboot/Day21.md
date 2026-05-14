## Day21 总结

### day21 复习
将 CLI 从“参数驱动工具”升级为“交互式工具”

### 1️⃣ 今天学了什么

* 输入校验机制（get_valid_input / get_valid_index）
* CLI 交互模式（input + while 循环）
* 命令无参数 → 自动进入交互输入
* 操作菜单设计（list → 选择操作）
* UI index vs 数据 index 的区别
* 用户行为驱动的 CLI 设计
* 输入错误处理（防崩 / 重试）

---

### 2️⃣ 核心代码

```python
def get_valid_index(max_index: int) -> int:
    while True:
        value = input(f"请输入任务编号 (1 ~ {max_index}): ").strip()

        if not value.isdigit():
            print("❌ 必须输入数字")
            continue

        index = int(value)

        if 0 < index <= max_index:
            return index - 1

        print("❌ 编号超出范围")
```

```python
ui_index = get_valid_index(len(tasks))
task = tasks[ui_index]
manager.mark_done(task.index)
```

---

### 3️⃣ 我理解的本质（最重要❗）

* CLI 不只是“执行命令”，而是“与用户交互”
* 用户输入是不可控的，必须做校验
* UI 展示顺序 ≠ 数据真实顺序
* 操作应该基于“用户看到的内容”而不是“内部结构”

👉 核心思想：
好 CLI = 安全输入 + 清晰引导 + 正确数据流

---

### 4️⃣ 我踩的坑

❌ UI index 和 task.index 混用导致操作错误
❌ 过滤 / 排序后仍使用原始 index
❌ 直接 int(input()) 导致崩溃
❌ get_valid_input 默认参数写成 None
❌ edit priority 拼写错误（mediem）
❌ action 输入没有校验
❌ 用递归刷新 list（后续需优化为循环）

---

### 5️⃣ 明天要做什么

进入“结构优化 + 工程化”：

* 去掉递归 → 改为 while 循环结构
* 抽取共通逻辑（get_filtered_tasks）
* 数据获取与展示彻底分离
* CLI 结构优化（更清晰的 flow）
* 输出和错误提示统一格式

---

### Day21 一句话总结

👉 CLI 的本质是“用户交互系统”，而不是“命令执行脚本”