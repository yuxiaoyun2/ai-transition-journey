#返回第一个匹配项，没有就返回 None
def first_keyword(data: list[str], key: str) -> str | None:
    for item in data:
        if key.lower().lower():
            return item
    return None


data = ["Apple", "banana", "APP"]

print(first_keyword(data, "app"))