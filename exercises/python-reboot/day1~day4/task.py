from dataclasses import dataclass, asdict
@dataclass
class Task:
    index: int
    title: str
    done: bool = False
    
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
            
        done = data.get("done", False)
        done = bool(done)
        
        return cls(
            index=data.get("index", fixed_index),
            title=data["title"],
            done=done
        )
        
    def display(self) -> str:
        mark = "[x]" if self.done else "[ ]"
        return f"{self.index + 1}. {mark} {self.title}"
    
    def done_task(self):
        self.done = True