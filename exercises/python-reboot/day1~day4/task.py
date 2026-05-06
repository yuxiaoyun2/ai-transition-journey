from dataclasses import dataclass, asdict
VALID_PRIORITIES = ["high", "medium", "low"]
@dataclass
class Task:
    index: int
    title: str
    done: bool = False
    priority:str = "medium"
    
    def __post_init__(self):
        if self.priority not in VALID_PRIORITIES:
            raise ValueError("invalid priority")
        
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls,data, index=0):
        if not isinstance(data, dict):
            raise ValueError("invalid item type")
        if "title" not in data or not isinstance(data["title"], str):
            raise ValueError("title is required")
        
        raw_index = data.get("index", index)
        try:
            fixed_index = int(raw_index)
        except (TypeError, ValueError):
            fixed_index = index
            
        done = bool(data.get("done", False))
        
        priority = data.get("priority", "medium")
        if priority not in VALID_PRIORITIES:
            priority = "medium"
        
        return cls(
            index=fixed_index,
            title=data["title"],
            done=done,
            priority = priority
        )
        
    def display(self) -> str:
        return f"{self.index + 1}. [{'x' if self.done else ' '}] {self.title} ({self.priority})"
    
    def mark_done(self):
        self.done = True