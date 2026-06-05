import argparse
from memo_manager import MemoManager


def create_parser():
    parser = argparse.ArgumentParser(description=" memo CLI")
    parser.add_argument("--file", default="memos.json")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    add_parser = subparsers.add_parser("add", help="add a new memo")
    add_parser.add_argument("title", type=str, help="memo title")
    add_parser.add_argument("content", type=str, help="memo content")

    delete_parser = subparsers.add_parser("delete", help="delete a memo")
    delete_parser.add_argument("index", type=int, help="memo index")

    edit_parser = subparsers.add_parser("edit", help="edit memo")
    edit_parser.add_argument("index", type=int, help="memo index")
    edit_parser.add_argument("--title", type=str, help="memo title")
    edit_parser.add_argument("--content", type=str, help="memo content")

    search_parser = subparsers.add_parser("search", help="search memo")
    search_parser.add_argument("--index", type=int, help="memo index")
    search_parser.add_argument("--keyword", type=str, help="memo keyword")

    subparsers.add_parser("list", help="memo list")

    return parser


def main():
    parser = create_parser()

    args = parser.parse_args()

    manager = MemoManager(file_path=args.file)

    if args.command == "add":
        memo = manager.add_memo(args.title, args.content)
        if memo:
            print(f"the memo is added success! title: {memo.title}")

    if args.command == "list":
        memos = manager.list_memo()
        if len(memos) == 0:
            print("No memos found!")
            return
        for memo in memos:
            print(f"{memo.index + 1}. [{memo.created_at}]{memo.title}")
            print(f"    {memo.content}")

    if args.command == "edit":
        memo = manager.edit_memo(args.index - 1, args.title, args.content)
        if memo:
            print(f"the memo is edited success! title: {memo.title}")
        else:
            print("memo not found!")

    if args.command == "delete":
        memo = manager.delete_memo(args.index - 1)
        if memo:
            print(f"the memo is deleted success! title: {memo.title}")
        else:
            print("memo not found!")

    if args.command == "search":
        index = args.index
        keyword = args.keyword
        while index is None and keyword is None:
            print("please provide at least one index or keyword.")
            index_input = input("index (please Enter to skip): ").strip()
            keyword_input = input("keyword (please Enter to skip)").strip()

            if index_input:
                try:
                    index = int(index_input)
                except ValueError:
                    print("index must be a number.")
                    continue

            if keyword_input:
                keyword = keyword_input

            memos = manager.search_memo(
                index=index - 1 if index is not None else None, keyword=keyword
            )
            if len(memos) == 0:
                print("No memo matched the conditions")
            for memo in memos:
                print(f"{memo.index + 1}. [{memo.created_at}] {memo.title}")
                print(f"    {memo.content}")


if __name__ == "__main__":
    main()
