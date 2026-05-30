import json
import os

class ChatStorage:
    def __init__(self, session: str = "default"):
        self.file_path = f"{session}.json"
    
    def save(self, messages: list[dict]):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
            
    def load(self)->list[dict]:
        if not os.path.exists(self.file_path):
            return[]
        
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    