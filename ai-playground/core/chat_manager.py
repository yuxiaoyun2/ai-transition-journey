from .storage import ChatStorage


class ChatManager:
    def __init__(self, system_prompt: str, storage: ChatStorage):
        self.storage = storage
        self.messages = self.storage.load()

        self._ensure_single_system_message(system_prompt)

    def add_user_message(self, text: str):
        self.messages.append({"role": "user", "content": text})
        self.storage.save(messages=self.messages)

    def add_ai_message(self, text: str):
        self.messages.append({"role": "assistant", "content": text})
        self.storage.save(messages=self.messages)

    def get_messages(self):
        return self.messages

    def trim_messages(self):
        MAX_MESSAGES = 11
        if len(self.messages) > MAX_MESSAGES:
            self.messages.pop(1)
            self.messages.pop(1)
        self.storage.save(self.messages)

    def reset_messages(self):
        system_message = self.messages[0] if self.messages else None

        if system_message:
            self.messages = [system_message]

        else:
            self.messages = []

        self.storage.save(self.messages)

    def get_last_user_message(self):
        return next(
            (msg for msg in reversed(self.messages) if msg["role"] == "user"), None
        )

    def get_user_messages_count(self) -> int:
        return sum(1 for msg in self.messages if msg["role"] == "user")

    def get_last_n_messages(self, n: int) -> list[dict]:
        system_message = self.messages[0] if self.messages else None

        recent = self.messages[-n:] if n > 0 else []

        if system_message and system_message not in recent:
            return [system_message] + recent

        return recent

    def show_last_5_messages(self):
        msgs = self.messages[1:][-5:]
        for msg in msgs:
            role = "you: " if msg["role"] == "user" else "AI: "
            print(f"{role} {msg['content']}")

    def _ensure_single_system_message(self, system_prompt):
        if self.messages:
            msg = self.messages[0]
            if msg.get("role") == "system" and msg.get("content") == system_prompt:
                return

        self.messages = [{"role": "system", "content": system_prompt}]
        self.storage.save(self.messages)

    def change_role(self, system_prompt: str):
        if not self.messages:
            self.messages = [{"role": "system", "content": system_prompt}]
        elif self.messages[0].get("role") == "system":
            self.messages[0] = {"role": "system", "content": system_prompt}
        else:
            self.messages.insert(0, {"role": "system", "content": system_prompt})

        self.storage.save(self.messages)

    def search_messages(self, keyword: str) -> list:
        results = []

        for msg in self.messages:
            content = msg.get("content", "")
            if keyword.lower() in content.lower():
                results.append(msg)

        return results
