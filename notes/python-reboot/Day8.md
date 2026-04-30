## Day8 总结

### 1️⃣ 今天学了什么

* lambda（匿名函数）
* sorted（排序）
* filter（筛选）
* 数据处理组合（filter + sorted）
* CLI 参数驱动数据逻辑（--undone / --sort / --keyword）

---

### 2️⃣ 核心代码

```python
sorted(tasks, key=lambda task: task.index)
```

```python
filter(lambda task: not task.done, tasks)
```

```python
def get_tasks(self, undone=False, done=False, keyword=None, sort=None):
    tasks = self.tasks

    if undone:
        tasks = filter(lambda task: not task.done, tasks)
    elif done:
        tasks = filter(lambda task: task.done, tasks)

    if keyword:
        tasks = filter(
            lambda task: keyword.lower() in task.title.lower(),
            tasks
        )

    if sort == "asc":
        tasks = sorted(tasks, key=lambda task: task.index)
    elif sort == "desc":
        tasks = sorted(tasks, key=lambda task: task.index, reverse=True)

    return list(tasks)
```

```python
list_parser.add_argument("--undone", action="store_true")
list_parser.add_argument("--done", action="store_true")
list_parser.add_argument("--sort", choices=["asc", "desc"])
list_parser.add_argument("--keyword", type=str)
```

---

### 3️⃣ 我理解的本质（最重要❗）

* lambda = “临时函数”，用于描述规则（排序 / 筛选）
* lfilter = 只保留满足条件的数据
* lsorted = 按规则排序数据（不会修改原数据）
* l核心模式：
```python
tasks = 原始数据
tasks = filter(...)
tasks = sorted(...)
return list(tasks)
```
本质是：数据流（data pipeline）处理

---

### 4️⃣ 我踩的坑

* sorted(tasks, lambda ...) → 忘记 key=
* filter(...) 直接返回 → 不是 list
* 写成 [filter(...)] → 结构错误
* tasks 未初始化 → UnboundLocalError
* keyword=None → None in string 报错
* 多个条件覆盖数据（没有用同一个 tasks）
* CLI 参数写成 subcommand（设计错误）

---

### 5️⃣ 明天要做什么

* 优化 CLI（更像真实工具）
* 错误提示优化（用户体验）
* index 设计优化（删除后的编号问题）
* 输出格式优化（更清晰）
* 代码重构（职责更清晰）
