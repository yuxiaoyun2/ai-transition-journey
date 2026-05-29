from storage import ChatStorage

class ChatManager:
    def __init__(self, system_prompt: str, storage: ChatStorage):
        self.storage = storage
        self.messages = self.storage.load()
        
        if not self.messages:
            self.messages = [
                {"role": "system", "content": system_prompt}
            ]
            self.storage.save(messages= self.messages)
        
    
    def add_user_message(self, text: str):
        self.messages.append({"role": "user", "content": text})
        self.storage.save(messages= self.messages)
        
    def add_ai_message(self, text: str):
        self.messages.append({"role":"assistant", "content": text})
        self.storage.save(messages= self.messages)
        
    def get_messages(self):
        return self.messages
    
    def trim_messages(self):
        if len(self.messages) > 11:
            self.messages.pop(1)
            self.messages.pop(1)
        self.storage.save(self.messages)