## Day13 总结

### day13复习
```python
正常路径决定功能，异常路径决定质量
```

### 1️⃣ 今天学了什么

* CLI 测试（测试命令行工具）
* 使用 sys.argv 模拟用户输入
* 使用 capsys 捕获输出（print）
* 实现端到端测试（add → list）
* 支持 CLI 参数注入（--file）

---

### 2️⃣ 核心代码

```python
sys.argv = ["todo.py", "--file", str(file_path), "list"]
main()
```

```python
captured = capsys.readouterr()
assert "タスクはありません" in captured.out
    ...
```

```python
def test_cli_add_and_list(tmp_path, capsys):
    file_path = tmp_path / "todo.json"

    sys.argv = ["todo.py", "--file", str(file_path), "add", "study"]
    main()

    sys.argv = ["todo.py", "--file", str(file_path), "list"]
    main()

    captured = capsys.readouterr()

    assert "study" in captured.out
```

---

### 3️⃣ 我理解的本质（最重要❗）

* CLI 是用户真实入口，不测试 = 产品不可控
* sys.argv = 模拟用户输入
* capsys = 捕获程序输出
* 测试不仅验证逻辑，还验证“用户看到的结果”

👉 核心思想：
```python
函数测试保证逻辑，CLI 测试保证产品行为
```

---

### 4️⃣ 我踩的坑

* pytest 找不到命令（需要用 python3 -m pytest）
* CLI 写死 todo.json → 测试污染数据
* 没有支持 --file 参数
* 不理解 sys.argv 的作用
* capsys 不会用

---

### 5️⃣ 明天要做什么

* 数据结构扩展（Task 升级）
* JSON 兼容（老数据不崩）
* CLI 参数扩展
* 测试如何跟着改

---

### Day13 一句话总结

👉 从“写函数” → “测试整个产品行为”