
def get_valid_priority() -> str:
    
    while True:
        priority = input("优先级（high/medium/low）: ").strip().lower()
        
        if priority == "":
            return None
        
        if priority in ["high", "medium", "low"]:
            return priority
    
        print("输入有误， 请重新输入")