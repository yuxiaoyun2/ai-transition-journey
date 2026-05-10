
def update_task(task: dict, title: str = None, priority: str = None) -> dict:
    if title is None and priority is None:
        raise ValueError("至少更新一个字段")
    
    if title is not None:
        task["title"] = update_title(task["title"], title)
        
    if priority is not None:
        task["priority"] = update_priority(task["priority"], priority)
    
    return task
    
def update_title(old_title: str, new_title: str) -> str:
    new_title = new_title.strip()
    if not new_title:
        raise ValueError("标题不能为空")
    
    if new_title == old_title.strip():
        return old_title
    
    return new_title

def update_priority(old_priority:str, new_priority:str) -> str:
    if not new_priority:
        raise ValueError("优先级不能为空")

    if new_priority not in ["high", "medium", "low"]:
        raise ValueError("优先级必须是 high/medium/low")
    
    if old_priority == new_priority:
        return old_priority
    
    return new_priority