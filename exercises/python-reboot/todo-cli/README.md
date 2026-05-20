> A structured CLI project built during my transition into AI engineering.

# 📝 Todo CLI Tool

A lightweight command-line task management tool built with Python.

---

## 🚀 Overview

This project is a simple yet structured CLI application
designed to practice clean architecture and Python backend fundamentals.

It demonstrates:

* CLI design with `argparse`
* Object-oriented modeling
* Separation of concerns
* Logging and error handling

---

## ✨ Features

* Add / list / edit / remove tasks
* Mark tasks as done
* Filter by status / keyword / priority
* Sort tasks (asc / desc / priority / smart)
* Interactive CLI mode
* File-based logging system

---

## 🧱 Project Structure

```
todo-cli/
│
├── todo.py            # CLI entry point
├── todo_manager.py    # Business logic layer
├── task.py            # Task model
├── todo.json.example  # Example data
├── todo.log           # Log file
│
├── README.md
└── .gitignore
```

---

## 📦 Setup

Copy the example data file:

```bash
cp todo.json.example todo.json
```

---

## ▶️ Usage

### Add a task

```bash
python todo.py add --title "Study Python" --priority high
```

### List tasks

```bash
python todo.py list
```

### Mark task as done

```bash
python todo.py done 1
```

### Remove a task

```bash
python todo.py remove 1
```

### Edit a task

```bash
python todo.py edit 1 --title "New Title" --priority low
```

---

## 🧪 Example

```bash
python todo.py add --title "Study Python" --priority high
python todo.py add --title "Buy milk"
python todo.py list
```

Output(Japanese UI):

```
=== 未完了 (2) ===
[ ] 1. Study Python
[ ] 2. Buy milk

合計: 2
```

---

## 🪵 Logging

Logs are automatically written to `todo.log`.

Example:

```
2026-xx-xx 12:00:00 [INFO] [todo_manager] task added: Study Python
2026-xx-xx 12:01:00 [ERROR] [todo_manager] mark_done failed: index=10
```

---

## 🧠 Design Highlights

* Task state is managed via object fields (`done`, `priority`)
* UI output is separated from data representation
* Business logic is centralized in `TodoManager`
* Logging is handled using Python `logging` module
* Input validation ensures robust CLI interaction

---

## 📌 Future Improvements

* Add logging levels (DEBUG / WARNING)
* Support database storage (SQLite)
* Improve test coverage
* Package as installable CLI tool

---

## 👤 Author

YOYO | Tokyo Reboot Project 🚀
