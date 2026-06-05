from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Memo:
    index: int
    title: str
    content: str
    created_at: str
    updated_at: str
    status: str = "normal"

    def to_dict(self):
        return asdict(self)

    @classmethod
    def create(cls, index: int, title: str, content: str):
        now = datetime.now().isoformat(timespec="seconds")
        return cls(
            index=index, title=title, content=content, created_at=now, updated_at=now
        )
