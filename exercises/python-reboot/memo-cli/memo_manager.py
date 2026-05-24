from memo_model import Memo
import json
import os
from typing import Optional 
class MemoManager:
    
    def __init__(self, file_path:str = "memos.json"):
        self.file_path = file_path
        self.memos = []
        self.load_memo()
        
    def load_memo(self):
        if not os.path.exists(self.file_path):
            self.memos = []
            return

        try:    
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.memos = [Memo(**item) for item in data]
        except (json.JSONDecodeError, TypeError):
            print("⚠️ JSONファイルが破損していたため、空のリストにリセットしました。")
            self.memos = []
    
    def save_memo(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([m.to_dict() for m in self.memos], f, ensure_ascii=False, indent=2)
    
    def add_memo(self, title:str, content: str) -> Memo:
        index = len(self.memos)
        memo = Memo.create(index, title, content)
        self.memos.append(memo)
        self.save_memo()
        return memo
        
    def delete_memo(self, index: int):
        memo = self.search_memo(index)
        if not memo:
            return None
        
        self.memos = [memo for memo in self.memos if memo.index != index]
        self.save_memo()
        return memo
    
    def edit_memo(self, index: int, title: str = None, content: str = None) -> Optional[Memo]:
        memo = self.search_memo(index)
        if memo is None:
            return None
        
        if title is not None and title != memo.title:
            memo.title = title
        if content is not None and content != memo.content:
            memo.content = content
            
        self.save_memo()
        return memo
    
    def search_memo(self, index: int = None, keyword: str = None) -> list[Memo]:
        result = []
        for memo in self.memos:
            if index is not None and index != memo.index:
                continue
            
            if keyword is not None:
                if keyword not in memo.title and keyword not in memo.content:
                    continue
                
            result.append(memo)
        return result     
        
    def list_memo(self):
        return self.memos