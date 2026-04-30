## Day7 总结

### 1️⃣ 今天学了什么

* JSON 持久化（json.dump / json.load）
* 数据模型转换（to_dict / from_dict）
* 异常处理（try / except）
* CLI 输入保护（防止程序崩溃）

---

### 2️⃣ 核心代码

```python
json.dump([t.to_dict() for t in self.tasks], f, ensure_ascii=False, indent=2)
```

```python
@classmethod
def from_dict(cls, data, index=0):
    return cls(
        index=data.get("index", index),
        title=data["title"],
        done=data.get("done", False)
    )
```

---

### 3️⃣ 我理解的本质（最重要❗）

* JSON 只能存基础类型（dict / list），不能存 class
* to_dict = 对象 → dict（用于存储）
* from_dict = dict → 对象（用于恢复）
* 程序必须假设数据可能是错误的（需要校验和容错）

---

### 4️⃣ 我踩的坑

* 忘记 return → 函数返回 None
* 使用 `is not int` 判断类型（错误）
* index 可能为 None → display 报错
* JSON 数据缺字段 → KeyError 崩溃
* CLI 参数不足 → IndexError

---

### 5️⃣ 明天要做什么

* 学 lambda / sorted / filter
* 用在 Todo 项目（排序 / 搜索）
* 提升代码表达能力
