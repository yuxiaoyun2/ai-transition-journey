
import os
from dotenv import load_dotenv
import argparse
from config import ROLES
from chat_manager import ChatManager
from ai_client import AIClient
from storage import ChatStorage

def create_parser():
    parser = argparse.ArgumentParser(description="AI CLI")
    parser.add_argument("--role", default="default", choices=list(ROLES.keys()))
    parser.add_argument("--session", type=str, default="default")
    parser.add_argument("--list-sessions", action="store_true")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    role_key = args.role
    session = args.session
    
    if not session.strip():
        print("session can't be empty (e.g. --session work)")
        return
    
    storage = ChatStorage(session)
    
    if args.list_sessions:
        sessions = storage.list_sessions()
        
        if not sessions:
            print("まだ session はありません")
            return
        
        print("have sessions: ")
        for s in sessions:
            print(f"- {s}")
        return
    
    system_prompt = ROLES.get(role_key, ROLES["default"])
    
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")  
    
    chat_manager = ChatManager(system_prompt, storage)
    ai_client = AIClient(api_key)
    
    if not api_key:
        print("OPENAI_API_KEY が設定されていません")
        return
    
    print(f"session: {session}")
    print(f"role: {role_key}")
    print("AI CLIを開始します。終了するには exit と入力してください。")
    
    while True:
    
        chat_manager.trim_messages()
        
        question = input("you: ")
        
        if question=="exit":
            print("保存して終了します")
            break
        
        if question=="/clear":
            chat_manager.clear_messages()
            print("会話履歴をクリアしました")
            continue
    
        if question=="/history":
            chat_manager.show_last_5_messages()
            continue
    
        chat_manager.add_user_message(question)
    
        ai_answer = ai_client.chat(messages=chat_manager.get_messages())
        print("AI: ",ai_answer)
    
        chat_manager.add_ai_message(ai_answer)
    
    
if __name__ == "__main__":
    main()