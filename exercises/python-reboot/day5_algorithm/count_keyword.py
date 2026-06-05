# 返回数量
def count_keyword(data, key: str):
    count = 0
    for item in data:
        if key.lower() in item.lower():
            count += 1

    return count


if __name__ == "__main__":
    data = ["Apple", "banana", "APP"]
    print(count_keyword(data, "app"))
