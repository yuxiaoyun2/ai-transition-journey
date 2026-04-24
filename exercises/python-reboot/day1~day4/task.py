from dataclasses import dataclass, asdict
@dataclass
class Task:
    index: int
    title: str
    done: bool = False
    
    def display(self) -> str:
        mark = "✅"  if self.done else "❌" 
        return f"{self.index +1 } {self.title} {mark}"
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls,data, index=None):
        return cls(
            index=data.get("index", index),
            title=data["title"],
            done=data.get("done", False)
        )