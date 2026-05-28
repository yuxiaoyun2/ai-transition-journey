class ChatManager:
    def __init__(self, system_prompt: str):
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]
    
    def add_user_message(self, text: str):
        self.messages.append({"role": "user", "content": text})
        
    def add_ai_message(self, text: str):
        self.messages.append({"role":"assistant", "content": text})
        
    def get_messages(self):
        return self.messages
    
    def trim_messages(self):
        if len(self.messages) > 11:
            self.messages.pop(1)
            self.messages.pop(1)