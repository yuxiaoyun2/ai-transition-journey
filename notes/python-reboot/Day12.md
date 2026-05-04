## Day12 总结

### day12复习
```python
正常路径决定功能，异常路径决定质量
```

### 1️⃣ 今天学了什么

* 异常测试（exception test）
* 使用 pytest.raises 验证错误行为
* 边界条件测试（invalid index / 空输入）
* 补全 TodoManager 的测试覆盖
* 区分“正常路径测试”和“异常路径测试”

---

### 2️⃣ 核心代码

```python
def test_add_task(tmp_path):
    def test_mark_done_invalid_index(tmp_path):
    manager = TodoManager(file_path=str(tmp_path/"test.json"))

    manager.add_task("study")

    with pytest.raises(ValueError):
        manager.mark_done(999)
```

```python
def test_get_tasks_undone(tmp_path):
    def test_remove_invalid_index(tmp_path):
    manager = TodoManager(file_path=str(tmp_path/"test.json"))

    manager.add_task("study")

    with pytest.raises(ValueError):
        manager.remove_task_by_index(999)
    ...
```

```python
def test_get_tasks_keyword(tmp_path):
    def test_keyword_empty(tmp_path):
    manager = TodoManager(file_path=str(tmp_path/"test.json"))

    manager.add_task("study")

    tasks = manager.get_tasks(keyword="")

    assert len(tasks) == 1
```

---

### 3️⃣ 我理解的本质（最重要❗）

* 不仅要测试“能成功”，还要测试“会失败”
* 异常是 API 行为的一部分
* 测试定义了系统的边界
* 边界测试比正常测试更有价值

👉 核心思想：
```python
正常路径保证功能，异常路径保证稳定性
```

---

### 4️⃣ 我踩的坑

* 忘记测试异常路径（只测 happy path）
* 使用固定 test.json → 数据污染
* pytest 运行目录错误 → 找不到测试
* IDE 报 pytest import 错误（解释器不一致）

---

### 5️⃣ 明天要做什么

* CLI 测试（测试 todo.py 输出）
* 学习 pytest 捕获 stdout（capfd / capsys）
* 验证 CLI 参数行为（--undone / --sort）
* 让整个工具“可测试”

---

### Day12 一句话总结

👉 从“代码能跑” → “代码在任何情况下都可控”