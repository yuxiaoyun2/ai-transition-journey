## Day14 总结

### day14复习
```python
正常路径决定功能，异常路径决定质量
```

### 1️⃣ 今天学了什么

* 数据模型扩展（Task 增加 priority）
* CLI 参数设计（--priority + choices）
* dataclass 初始化钩子（__post_init__）
* 数据校验分层（CLI 校验 + 模型校验）
* JSON 向后兼容（老数据处理）
* CLI 测试（正常 + 异常）

---

### 2️⃣ 核心代码

```python
add_parser.add_argument(
    "--priority",
    choices=["high", "medium", "low"],
    default="medium"
)
```

```python
def __post_init__(self):
    if self.priority not in VALID_PRIORITIES:
        raise ValueError("invalid priority")
```

```python
priority = data.get("priority", "medium")
if priority not in VALID_PRIORITIES:
    priority = "medium"
```

```python
def get_tasks(..., priority=None):
    if priority:
        tasks = filter(lambda task: task.priority == priority, tasks)
```

```python
with pytest.raises(SystemExit):
    main()
```
---

### 3️⃣ 我理解的本质（最重要❗）

* CLI 是输入边界 → 负责用户输入校验
* 数据模型是核心 → 必须自我保护（post_init）
* JSON 数据不可信 → 必须做兼容处理
* 一个功能不是一处修改，而是多层协同

👉 核心思想：
边界校验 + 核心防御 + 数据兼容 = 稳定系统

---

### 4️⃣ 我踩的坑

* "priority" 写成字符串（变量错误）
* priority 拼写错误（mediun / " low"）
* list 命令错误设置 default → 导致默认过滤
* CLI 参数没有正确传入 manager
* 用合法值测试异常（逻辑错误）
* 忘记 from_dict 做数据修复

---

### 5️⃣ 明天要做什么

进入“产品级能力”：

* priority 排序规则（high > medium > low）
* 多条件组合查询（priority + undone + keyword）
* 更接近真实业务逻辑

---

### Day14 一句话总结

👉 数据模型不是存数据的，是保证数据正确的