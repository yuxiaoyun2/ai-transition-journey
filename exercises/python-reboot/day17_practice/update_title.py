
class updateTitle:
    def update_title(old_title: str, new_title: str) -> str:
        new_title = new_title.strip()
        if not new_title:
            raise ValueError("标题不能为空")
    
        if new_title == old_title.strip():
            return old_title
    
        return new_title