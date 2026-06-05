# 去重并保持顺序：


def unique_keyword(data: list[str]) -> list[str]:
    result = []
    for item in data:
        if item not in result:
            result.append(item)
    return result


data = ["apple", "banana", "apple", "APP"]
print(unique_keyword(data))
