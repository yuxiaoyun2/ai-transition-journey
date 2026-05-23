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
    search_parser.add_argument("index", type=int, help="memo index")
    
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
        for memo in memos:
            print(f"{memo.index + 1}. {memo.title}, {memo.content}")
            
    if args.command == "edit":
        memo = manager.edit_memo(args.index - 1 , args.title, args.content)
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
        memo = manager.search_memo(args.index - 1)
        if memo:
            print(f"title: {memo.title}")
            print(f"content: {memo.content}")
        else:
            print("memo not found!")
            
if __name__ == "__main__":
    main()