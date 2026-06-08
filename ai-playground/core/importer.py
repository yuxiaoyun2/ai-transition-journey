import json
import os


class ChatImporter:
    def import_json(self, filepath: str) -> list:
        if not os.path.exist(filepath):
            raise FileNotFoundError("指定されたファイルが存在しません")

        with open(filepath, "r", encoding="utf-8") as f:
            messages = json.load(f)

            if not isinstance(messages, list):
                raise ValueError("JSON形式が正しくありません")

            for msg in messages:
                if not isinstance(msg, dict):
                    raise ValueError("メッセージ形式が正しくありません")

                if "role" not in msg or "content" not in msg:
                    raise ValueError("role または content　がありません")

        return messages
