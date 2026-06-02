from openai import OpenAI

class AIClient:
    def __init__(self, api_key:str):
        self.client = OpenAI(api_key=api_key)
        
    def chat(self, messages: list[dict]) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content
    
    def stream_chat(self, messages):
        stream = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True
        )
        
        full_text = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            
            if delta:
                print(delta, end="", flush=True)
                full_text += delta
        print()
        return full_text
                