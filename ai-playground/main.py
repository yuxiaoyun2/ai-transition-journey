import os
from dotenv import load_dotenv
import argparse
from config import ROLES
from core.chat_manager import ChatManager
from core.storage import ChatStorage
from core.ai_client import AIClient
from cli.cli_utils import validate_args, show_config, show_help
from core.exporter import ChatExporter
from core.importer import ChatImporter


def create_parser():
    parser = argparse.ArgumentParser(description="AI CLI")
    parser.add_argument("--role", default="default", choices=list(ROLES.keys()))
    parser.add_argument("--session", type=str, default="default")
    parser.add_argument("--list-sessions", action="store_true")

    parser.add_argument("--model", type=str, default="gpt-4o-mini")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--max-tokens", type=int, default=500)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    try:
        validate_args(args)
    except ValueError as e:
        print(f"ERROR: {e}")
        return

    session = args.session
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

    role_key = args.role
    system_prompt = ROLES.get(role_key, ROLES["default"])

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("OPENAI_API_KEY が設定されていません")
        return

    chat_manager = ChatManager(system_prompt, storage)
    ai_client = AIClient(api_key, args.model, args.temperature, args.max_tokens)
    exporter = ChatExporter()
    importer = ChatImporter()

    show_config(session, role_key, args.model, args.temperature, args.max_tokens)

    print("AI CLIを開始します。終了するには exit と入力してください。")

    while True:

        question = input("you: ")
        if not question.strip():
            continue

        if question in ["exit", "/exit"]:
            print("保存して終了します")
            break

        if question == "/export":
            filepath = exporter.export_markdowm(session, chat_manager.get_messages())
            print(f"会話履歴をエクスポートしました: {filepath}")
            continue

        if question == "/export-json":
            filepath = exporter.export_json(session, chat_manager.get_messages())
            print(f"会話履歴をJSONでエクスポートしました：{filepath}")
            continue

        if question.startswith("/import "):
            filepath = question.replace("/import ", "").strip()

            try:
                messages = importer.import_json(filepath)
                chat_manager.messages = messages
                chat_manager.storage.save(messages)
                print(f"会話履歴をインポートしました: {filepath}")
            except Exception as e:
                print(f"インポートに失敗しました： {filepath}")

            continue

        if question == "/summary":
            summary_prompt = {
                "role": "user",
                "content": "これまでの会話内容を日本語で簡潔に要約してください。",
            }

            summary_messages = chat_manager.get_messages() + [summary_prompt]

            try:
                summary = ai_client.chat(summary_messages)
                print("\n=== 会話要約 ===")
                print(summary)
                print("================\n")
            except Exception as e:
                print(f"要約に失敗しました: {e}")
            continue

        if question == "/reset":
            chat_manager.reset_messages()
            print("会話履歴をリセットしました")
            continue

        if question == "/history":
            chat_manager.show_last_5_messages()
            continue

        if question.strip() == "/role":
            print("available roles: ")
            for role in ROLES.keys():
                print(f"- {role}")
            continue

        if question.startswith("/role "):
            new_role = question.replace("/role ", "").strip()
            if new_role not in ROLES:
                print("存在しないroleです")
                continue

            if role_key == new_role:
                print("roleは変わりませんでした")
                continue

            system_prompt = ROLES[new_role]
            role_key = new_role
            chat_manager.change_role(system_prompt)
            print(f"roleを {new_role} に変更しました")
            continue

        if question.startswith("/session "):
            new_session = question.replace("/session ", "").strip()

            if not new_session:
                print("session can't be empty")
                continue

            if session == new_session:
                print("sessionは変わりませんでした")
                continue

            storage = ChatStorage(new_session)
            session = new_session
            chat_manager = ChatManager(system_prompt, storage)

            print(f"sessionを {new_session} に変更しました")
            continue

        if question == "/config":
            show_config(
                session, role_key, args.model, args.temperature, args.max_tokens
            )
            continue

        if question == "/help":
            show_help()
            continue

        chat_manager.add_user_message(question)
        chat_manager.trim_messages()

        print("AI: ", end="", flush=True)
        reply = ai_client.stream_chat(messages=chat_manager.get_messages())
        chat_manager.add_ai_message(reply)


if __name__ == "__main__":
    main()
