from dataclasses import dataclass
@dataclass
class Task:
    index: int
    title: str
    done: bool = False
    
    def display(self) -> str:
        mark = "✅"  if self.done else "❌" 
        return f"{self.title} {mark}"