
import os
from dotenv import load_dotenv
import argparse
from config import ROLES
from chat_manager import ChatManager
from ai_client import AIClient

def create_parser():
    parser = argparse.ArgumentParser(description="AI CLI")
    parser.add_argument("--role", default="default", choices=ROLES.keys())
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    role_key = args.role
    
    system_prompt = ROLES.get(role_key, ROLES["default"])
    
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("OPENAI_API_KEY が設定されていません")
        return

    chat_manager = ChatManager(system_prompt)
    ai_client = AIClient(api_key)
    
    while True:
    
        chat_manager.trim_messages()
        
        question = input("you: ")
    
        if question=="exit":
            print("終了します")
            break
    
        chat_manager.add_user_message(question)
    
        ai_answer = ai_client.chat(messages=chat_manager.get_messages())
        print("AI: ",ai_answer)
    
        chat_manager.add_ai_message(ai_answer)
    
    
if __name__ == "__main__":
    main()