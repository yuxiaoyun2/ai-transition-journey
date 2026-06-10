import os
from dotenv import load_dotenv
import argparse
from config import ROLES
from core.chat_manager import ChatManager
from core.storage import ChatStorage
from core.ai_client import AIClient
from cli.cli_utils import validate_args, show_config, show_help, parse_command
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


def handle_rename_session(command_args, session, storage):
    if len(command_args) != 2:
        print("使い方: /rename-session old_name new_name")
        return

    old_name, new_name = command_args

    if old_name == session:
        print("現在使用中のsession名は変更できません")
        return

    try:
        renamed = storage.rename_session(old_name=old_name, new_name=new_name)

        if renamed:
            print(f"session名を変更しました: {old_name} -> {new_name}")
        else:
            print("変更元のsessionが見つかりませんでした")

    except Exception as e:
        print(f"session名の変更に失敗しました: {e}")


def handle_switch_session(command_args, session, system_prompt):
    if len(command_args) != 1:
        print("使い方: /session session_name")
        return session, None, None

    new_session = command_args[0]

    if not new_session:
        print("session can't be empty")
        return session, None, None

    if session == new_session:
        print("sessionは変わりませんでした")
        return session, None, None

    storage = ChatStorage(new_session)
    chat_manager = ChatManager(system_prompt, storage)

    print(f"sessionを {new_session} に変更しました")

    return new_session, storage, chat_manager


def handle_delete_session(command_args, session, storage):
    if len(command_args) != 1:
        print("使い方: /delete-session session_name")
        return

    target_session = command_args[0]

    if not target_session:
        print("session名を入力してください")
        return

    if target_session == session:
        print("現在使用中のsessionは削除できません")
        return

    deleted = storage.delete_session(target_session)

    if deleted:
        print(f"sessionを削除しました: {target_session}")
    else:
        print("指定されたsessionが見つかりませんでした")


def handle_import_file(command_args, importer, chat_manager):
    if len(command_args) != 1:
        print("使い方： /import filepath")
        return

    filepath = command_args[0]

    try:
        messages = importer.import_json(filepath)
        chat_manager.messages = messages
        chat_manager.storage.save(messages)
        print(f"会話履歴をインポートしました: {filepath}")
    except Exception as e:
        print(f"インポートに失敗しました： {e}")


def handle_summary(chat_manager, ai_client):
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


def handle_search(command_args, chat_manager):
    if len(command_args) != 1:
        print("使い方： /search keyword")
        return

    keyword = command_args[0]
    results = chat_manager.search_messages(keyword=keyword)
    if not results:
        print("該当するメッセージが見つかりませんでした")
    else:
        print(f"\n=== 検索結果 （{len(results)}件）===")
        for i, msg in enumerate(results, 1):
            print(f"{i}. [{msg['role']}]")
            print(msg["content"])
            print("-" * 20)


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

        command, command_args = parse_command(question)

        if command in ["exit", "/exit"]:
            print("保存して終了します")
            break

        if command == "/export":
            filepath = exporter.export_markdown(session, chat_manager.get_messages())
            print(f"会話履歴をエクスポートしました: {filepath}")
            continue

        if command == "/export-json":
            filepath = exporter.export_json(session, chat_manager.get_messages())
            print(f"会話履歴をJSONでエクスポートしました：{filepath}")
            continue

        if command == "/import":
            handle_import_file(
                command_args=command_args, importer=importer, chat_manager=chat_manager
            )
            continue

        if command == "/summary":
            handle_summary(chat_manager=chat_manager, ai_client=ai_client)
            continue

        if command == "/search":
            handle_search(command_args=command_args, chat_manager=chat_manager)
            continue

        if command == "/stats":
            stats = chat_manager.get_stats()

            print("\n=== Chat Stats ===")
            print(f"total messages: {stats['total']}")
            print(f"system messages: {stats['system']}")
            print(f"user messages: {stats['user']}")
            print(f"assistant messages: {stats['assistant']}")
            print(f"characters: {stats['characters']}")
            print("==================\n")
            continue

        if command == "/delete-session":
            handle_delete_session(
                command_args=command_args, session=session, storage=storage
            )
            continue

        if command == "/rename-session":
            handle_rename_session(
                command_args=command_args, session=session, storage=storage
            )
            continue

        if command == "/reset":
            chat_manager.reset_messages()
            print("会話履歴をリセットしました")
            continue

        if command == "/history":
            chat_manager.show_last_5_messages()
            continue

        if command == "/role":
            print("available roles: ")
            for role in ROLES.keys():
                print(f"- {role}")
            continue

        if command == "/set-role":
            if len(command_args) != 1:
                print("使い方: /set-role role_name")
                continue

            new_role = command_args[0]
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

        if command == "/session":
            new_session, new_storage, new_chat_manager = handle_switch_session(
                command_args, session, system_prompt
            )

            if new_storage and new_chat_manager:
                session = new_session
                storage = new_storage
                chat_manager = new_chat_manager

            continue

        if command == "/config":
            show_config(
                session, role_key, args.model, args.temperature, args.max_tokens
            )
            continue

        if command == "/help":
            show_help()
            continue

        chat_manager.add_user_message(question)
        chat_manager.trim_messages()

        print("AI: ", end="", flush=True)
        reply = ai_client.stream_chat(messages=chat_manager.get_messages())
        chat_manager.add_ai_message(reply)


if __name__ == "__main__":
    main()
