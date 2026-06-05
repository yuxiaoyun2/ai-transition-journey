from openai import OpenAI


class AIClient:
    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def chat(self, messages: list[dict]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content

    def stream_chat(self, messages):
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        full_text = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content

            if delta:
                print(delta, end="", flush=True)
                full_text += delta
        print()
        return full_text
