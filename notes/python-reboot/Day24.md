## Day24 总结

### day24 复习
将自定义日志系统升级为 Python 标准 logging 模块，实现工程级日志管理

### 1️⃣ 今天学了什么

* 使用 logging 模块替代自定义 log（print → logging）
* 日志写入文件（todo.log）
* 日志格式配置（asctime / levelname / message）
* 日志等级（INFO / ERROR）
* logger 使用方式（模块级 logger）
* logging 与 print 的职责区分
* logging 错误排查（format 字段错误）

---

### 2️⃣ 核心代码

```python
import logging

logging.basicConfig(
    filename="todo.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)
```

```python
def mark_done(self, index: int):
    if 0 <= index < len(self.tasks):
        task = self.tasks[index]
        task.done = True
        self.save_tasks()
        logger.info(f"task done: {task.title}")
        return task

    logger.error(f"mark_done failed: index={index}")
    raise ValueError("task not found")
```

---

### 3️⃣ 我理解的本质（最重要❗）

* logging 是“系统行为记录”，不是用户输出
* print 和 logging 必须分离（UI vs 系统）
* logging 模块提供统一的日志规范（时间 / 等级 / 格式）
* 日志是“可观测性”的基础（debug / 追踪 / 排查问题）

👉 核心思想：
好系统 = 功能正确 + 行为可追踪

---

### 4️⃣ 我踩的坑

❌ format 写错字段（sactime → asctime）
❌ 误以为所有 print 都要换成 logging
❌ 尝试在 CLI 中直接使用 logger（职责混乱）
❌ log 写在 raise 之后（不会执行）
❌ log 信息不够具体（缺少 index / title）

---

### 5️⃣ 明天要做什么

进入“工程化升级”：

进入“项目收尾 + 工程化整理”：

* logger 升级（多等级：DEBUG / WARNING）
* 日志结构优化（模块名 / 文件分离）
* CLI 输出统一（更像真实工具）
* 项目 README 编写（项目说明 + 使用方法）
* 准备作为面试项目展示

---

### Day24 一句话总结

👉 使用 logging 模块实现系统行为可追踪