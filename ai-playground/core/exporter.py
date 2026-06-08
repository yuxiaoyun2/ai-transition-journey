import os
from datetime import datetime


class ChatExporter:

    def __init__(self, export_dir: str = "exports"):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)

    def export_markdowm(self, session: str, messages: list) -> str:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{session}_{now}.md"
        filepath = os.path.join(self.export_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("#AI chat Export\n\n")
            f.write(f"Session: {session}\n\n")

            for msg in messages:
                role = msg.get("role", "unknowm")
                content = msg.get("content", "")

                f.write(f"##{role}\n\n")
                f.write(content)
                f.write("\n\n")

        return filepath
