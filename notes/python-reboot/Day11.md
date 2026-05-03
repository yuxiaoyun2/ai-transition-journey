## Day11 总结

### day11复习
```python
没有测试的代码 = 不可控代码
```

### 1️⃣ 今天学了什么

* pytest 基本使用
* 单元测试（unit test）编写
* 使用 tmp_path 做测试隔离
* assert 进行结果验证
* 测试 TodoManager 核心业务逻辑

---

### 2️⃣ 核心代码

```python
def test_add_task(tmp_path):
    manager = TodoManager(file_path=str(tmp_path/"test.json"))

    manager.add_task("study")

    tasks = manager.get_tasks()

    assert len(tasks) == 1
    assert tasks[0].title == "study"
    assert tasks[0].done is False
```

```python
def test_get_tasks_undone(tmp_path):
    manager = TodoManager(file_path=str(tmp_path/"test.json"))

    manager.add_task("study")
    manager.add_task("sleep")

    manager.mark_done(0)

    tasks = manager.get_tasks(undone=True)

    assert len(tasks) == 1
    assert tasks[0].title == "sleep"
    ...
```

```python
def test_get_tasks_keyword(tmp_path):
    manager = TodoManager(file_path=str(tmp_path/"test.json"))

    manager.add_task("study")
    manager.add_task("dinner Sleep")

    tasks = manager.get_tasks(keyword="sleep")

    titles = [t.title for t in tasks]

    assert len(tasks) == 1 or len(tasks) == 2
    assert any("Sleep" in t or "sleep" in t for t in titles)
```

---

### 3️⃣ 我理解的本质（最重要❗）

* 测试不是为了“现在正确”，而是为了“未来不出问题”
* 每个测试应该是独立的（不能互相影响）
* tmp_path = 给每个测试一个干净环境
* 测试应该只验证一个行为（Single Responsibility）

👉 核心思想：
```python
写功能 → 写测试 → 以后敢改代码
```

---

### 4️⃣ 我踩的坑

* 使用同一个 test.json → 数据污染
* pytest 在错误目录运行 → 找不到测试
* 函数名没用 test_ 开头 → 不被识别
* 测试依赖执行顺序 → 不稳定
* 测试验证了太多逻辑（不够聚焦）

---

### 5️⃣ 明天要做什么

* 异常测试（invalid index / 边界情况）
* 测试覆盖率思维（覆盖更多路径）
* 优化 TodoManager（让它更易测试）
* 学习 mock（可选）

---

### Day10 一句话总结

👉 从“写代码” → 进入“写可验证、可维护的代码”