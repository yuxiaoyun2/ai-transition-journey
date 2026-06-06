# AI CLI Chat Tool

Pythonで作成したCLIベースのAIチャットツールです。

---

## Features

- AIとの対話
- role切り替え
- session管理
- JSONによる会話履歴の保存
- streaming出力
- token制限
- model / temperature / max_tokens の指定
- runtime command対応
- pre-commit + Black による自動フォーマット

---

## Project Structure

```plaintext
ai-playground/
├── main.py
├── config.py
├── core/
│   ├── ai_client.py
│   ├── chat_manager.py
│   └── storage.py
├── cli/
│   └── cli_utils.py
├── data/
│   └── sessions/
├── requirements.txt
└── .pre-commit-config.yaml
```

## Setup

```bash
python3 -m pip install -r requirements.txt
```

Create a `.env` file:
```env
OPENAI_API_KEY=your_api_key_here
```

## Quick Start

```bash
git clone <your-repo-url>
cd ai-playground
python3 -m pip install -r requirements.txt
python3 main.py --session demo
```

## Usage

```bash
python3 main.py --session default
```

パラメータ指定：
```bash
python3 main.py \
  --session study \
  --role teacher \
  --model gpt-4o-mini \
  --temperature 0.7 \
  --max-tokens 500
```

## Runtime Commands

```text
/help          show commands
/config        show current config
/role          list roles
/role xxx      change role
/session xxx   change session
/history       show recent history
/reset         reset conversation
/exit          exit CLI
```

## Development

コード整形：
```bash
python3 -m black .
```

pre-commit設定：
```bash
python3 -m pre_commit install
python3 -m pre_commit run --all-files
```

## Design

このプロジェクトでは、責務分離を意識しています。

- main.py: アプリケーションの入口
- core/: AI通信、会話管理、保存処理
- cli/: CLI表示、入力チェック、help表示
- data/: sessionデータ保存 

## What I Learned

- OpenAI APIの利用
- streaming responseの実装
- CLI引数設計
- JSON永続化
- token制限
- role/session設計
- Python package構造
- pre-commitによる開発フロー改善