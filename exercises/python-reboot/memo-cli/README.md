# Memo CLI Tool

## 概要
CLIでメモ管理ツールを開発しました。
コマンドラインからメモの追加・検索・編集・削除を行えるツールです。

## 使用技術
- Python
- argparse
- JSON
- dataclass

## 主な機能
- メモの追加 / 一覧表示
- キーワード検索およびインデックス検索
- 編集 / 削除

## 設計ポイント
- CLI、ビジネスロジック、データ構造を分離しました
- MemoManagerにロジックを集約し、責務を明確化しました
- JSONファイルを用いてデータの永続化を実現しました
- 将来的な拡張（GUIやAPI化）を考慮した構造にしました

## 工夫した点
- dataclassを使用してデータ構造をシンプルに定義しました
- to_dict / from_dict を実装し、オブジェクトとJSONの相互変換を行いました
- 入力チェックを行い、ユーザー入力エラー時でも処理が停止しないようにしました
- インデックスとキーワードの複数条件による検索機能を実装しました

## 今後の改善
- SQLiteへの移行
- ログ機能の追加
- GUI化 / API化

## Usage

```bash
# add a memo 
python memo.py add "title" "content"

# list all memos
python memo.py list

# search by keyword
python memo.py search --keyword python

# edit a memo
python memo.py edit 1 --title "new title"

# delete a memo
python memo.py delete 1