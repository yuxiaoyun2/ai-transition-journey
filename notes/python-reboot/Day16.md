## Day16 总结

### day16复习
排序不是一条规则，是规则链

### 1️⃣ 今天学了什么

* 多维排序（multi-key sorting）
* 业务排序规则设计（status + priority + index）
* key = tuple 的排序机制
* 容错设计（.get 默认值）
* CLI 支持复杂排序（smart）

---

### 2️⃣ 核心代码

```python
tasks = sorted(
    tasks,
    key=lambda task: (
        task.done,
        -priority_order.get(task.priority, 0),
        task.index
    )
)
```

---

### 3️⃣ 我理解的本质（最重要❗）

* 排序不是字段，是规则组合
* key 可以是 tuple → 多规则排序
* Python 按 tuple 逐级比较
* 数据必须可比较（字符串 → 数字）

👉 核心思想：
复杂排序 = 多维规则映射

---

### 4️⃣ 我踩的坑

* 用了 priority 而不是 task.priority
* 忘记排序是逐字段比较
* 没理解 False < True
* CLI 没加 smart

---

### 5️⃣ 明天要做什么

进入“产品体验阶段”：

* CLI 输出优化（格式更清晰）
* 分组显示（未完成 / 已完成）

---

### Day16 一句话总结

👉 排序不是一条规则，是规则链