
def get_by_keyword(data: list, keyword: str, ignore_case: bool = False):
    if ignore_case:
        return list(filter(lambda item: keyword in item.lower(), data))
    return list(filter(lambda item: keyword in item, data))


def get_by_keywords_or(data:list, keywords:list):
    keywords = [k.lower() for k in keywords]
    return [item for item in data if any(x in item.lower() for x in keywords)]


def get_by_keywords_and(data:list, keywords:list):
    keywords = [k.lower() for k in keywords]
    return [item for item in data if all(x in item.lower() for x in keywords)]

def get_by_keywords(data:list[str], keywords:list[str], mode:str):
    keywords = [k.lower() for k in keywords]
    
    result = []
    for item in data:
        item_lower = item.lower()
        
        if(mode == "and"):
            if all(x in item_lower for x in keywords):
                result.append(item)
        elif(mode == "or"):
            if any(x in item_lower for x in keywords):
                result.append(item)
        else:
            raise ValueError("mode must be 'and' or 'or'")
    return result


data = ["apple","banana", "avocado", "grape"]
result = get_by_keyword(data=data, keyword="a")
for item in result:
    print (item)

print ("###########################")  
data2 = ["Apple", "banana", "AVOCADO"]
result2 = get_by_keyword(data=data2,keyword="a",ignore_case=True)
for item in result2:
    print (item)

print ("###########################")     
data3 = ["Apple", "banana", "AVOCADO"]
keys = ["a", "e"]
result3 = get_by_keywords_or(data=data3,keywords=keys)
for item in result3:
    print (item)
    
print ("###########################")   
data4 = ["Apple", "banana", "AVOCADO"]
keys4 = ["a", "e"]
result4 = get_by_keywords(data=data4,keywords=keys4, mode="or")
for item in result4:
    print (item)