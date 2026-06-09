import json
import os


class ChatStorage:
    def __init__(self, session: str, base_dir: str = "data/sessions"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.file_path = os.path.join(self.base_dir, f"{session}.json")

    def save(self, messages: list[dict]):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

    def load(self) -> list[dict]:
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_sessions(self):
        if not os.path.exists(self.base_dir):
            return []

        sessions = []

        for filename in os.listdir(self.base_dir):
            if filename.endswith(".json"):
                session_name = filename.replace(".json", "")
                sessions.append(session_name)

        return sessions

    def delete_session(self, session_name: str) -> bool:
        filepath = os.path.join(self.base_dir, f"{session_name}.json")

        if not os.path.exists(filepath):
            return False

        os.remove(filepath)
        return True

    def rename_session(self, old_name: str, new_name: str) -> bool:
        old_path = os.path.join(self.base_dir, f"{old_name}.json")
        new_path = os.path.join(self.base_dir, f"{new_name}.json")

        if os.path.exists(new_path):
            raise FileExistsError("変更先のsessionはすでに存在します")

        if not os.path.exists(old_path):
            raise FileNotFoundError((f"session not found: {old_name}"))

        os.rename(old_path, new_path)
        return True
