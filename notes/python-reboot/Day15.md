## Day15 总结

### day15复习
排序不是字段，是业务规则

### 1️⃣ 今天学了什么

* 自定义排序规则（priority）
* 业务逻辑排序（不是技术字段排序）
* key + lambda 的实际应用
* CLI 参数扩展（--sort priority）
* 测试排序行为（顺序验证）

---

### 2️⃣ 核心代码

```python
priority_order = {
    "high": 3,
    "medium": 2,
    "low": 1
}

tasks = sorted(
    tasks,
    key=lambda task: priority_order.get(task.priority, 0),
    reverse=True
)
```

---

### 3️⃣ 我理解的本质（最重要❗）

* 计算机不理解“重要性”，必须定义规则
* 排序不是字段，而是业务逻辑
* key = 把复杂数据转成可比较值

👉 核心思想：
业务规则 = 数据 → 数值映射 → 排序

---

### 4️⃣ 我踩的坑

* "priority" 拼写错误（priotity）
* CLI sort 没加 priority
* CLI 测试读取输出行错误
* 只测字段，不测顺序

---

### 5️⃣ 明天要做什么

进入“高级工程能力”：

* 多条件排序（priority + index）
* 稳定排序（secondary sort）

---

### Day15 一句话总结

👉 排序不是字段，是业务规则