# 删除所有包含 key 的元素（忽略大小写）
def remove_keyword(data: list[str], key: str) -> list[str]:
    return [item for item in data if key.lower() not in item.lower()]


data = ["Apple", "banana", "APP"]

print(remove_keyword(data, "app"))
