from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = []

while True:
    
    if len(messages) > 10:
        messages.pop(0)
        
    question = input("you: ")
    
    if question=="exit":
        print("終了します")
        break
    
    messages.append({"role": "user", "content": question})
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    ai_answer = response.choices[0].message.content
    print("AI: ",ai_answer)
    
    messages.append({"role": "assistant", "content": ai_answer})
    