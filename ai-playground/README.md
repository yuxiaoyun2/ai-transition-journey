# AI CLI Chat Tool

## Overview

This project is a CLI-based AI chat tool built with Python and OpenAI API.

The project focuses on:

- session management
- role switching
- command-driven interaction
- maintainable architecture
- extensibility

---

## Features

- AI chat interaction
- Role switching
- Session management
- Chat history persistence
- Search
- Summary
- Import / Export
- Streaming output
- Token limit management
- Configurable model / temperature / max_tokens
- Runtime command
- pre-commit + Black

---

## Project Structure

```plaintext
├── ai-playground
│   ├── cli
│   │   └── cli_utils.py
│   ├── config.py
│   ├── core
│   │   ├── ai_client.py
│   │   ├── chat_manager.py
│   │   ├── exporter.py
│   │   ├── importer.py
│   │   └── storage.py
│   ├── data
│   │   └── sessions
│   ├── exports
│   ├── main.py
│   ├── README.md
│   └── requirements.txt
```

## Tech Stack

- Python
- OpenAI API
- argparse
- python-dotenv
- JSON
- Black
- pre-commit

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

Example with parameters：
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
/help
/config

/role
/set-role xxx

/session xxx
/rename-session old new
/delete-session xxx

/history
/search keyword 
/summary
/stats

/export
/import filepath

/reset 
/exit 
```

## Examples

```bash
/session work

/search OpenAI

/import backup.json

//rename-session work project

/delete-session old_session
```

## Development

Code formatting：                                                            
```bash
python3 -m black .
```

pre-commit setup：
```bash
python3 -m pre_commit install
python3 -m pre_commit run --all-files
```

## Design

The project separates responsibilities into:

- CLI Layer
- Business Logic Layer
- Data Persistence Layer

This design improves maintainability, readability, and extensibility.

## Architecture

```text
User Input
    ↓
CLI Layer
    ↓
Command Parser
    ↓
Chat Manager
    ↓
Storage / AI Client
    ↓
JSON Files / OpenAI API
```

## What I Learned

- OpenAI API integration
- Streaming response implementation
- Session management design
- Command parsing and handler pattern
- JSON persistence
- Token limit management
- CLI architecture design
- Separation of Concerns
- Development workflow using pre-commit and Black


## Future Improvements

- Command dispatch table
- SQLite persistence
- Better search capabilities
- Configuration management