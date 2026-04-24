#忽略大小写搜索
def search_keyword(data: list[str], key: str)-> list[str]:
    return [item for item in data if key.lower() in item.lower()]


if __name__ == "__main__":
    data = ["Apple","banana","APP"]
    print(search_keyword(data,"app"))