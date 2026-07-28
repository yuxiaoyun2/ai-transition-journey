# AI Agent Backend

## Overview

AI Agent Backend built with FastAPI and OpenAI Agents SDK.

This project demonstrates how to build an AI Agent capable of:

- Tool Calling
- Multi-step Tool Calling
- Structured Output
- Context Management
- Memory
- Simple RAG
- Layered Architecture

The project follows a clean architecture using Router / Service / Repository layers and demonstrates how an LLM interacts with external tools to complete user requests.

---

## Features

- AI Agent Chat API
- Task Management (CRUD)
- Tool Calling
- Multi-step Tool Calling
- Structured Output (Pydantic)
- Session Context
- Conversation Memory
- Simple Document Search (Simple RAG)
- Global Exception Handling
- Logging
- Dependency Injection
- Unit Tests

---

## Tech Stack

- Python 3.11
- FastAPI
- OpenAI Agents SDK
- Pydantic
- SQLAlchemy
- SQLite
- pytest

---

## Project Structure

```text
app
├── agents
├── tools
├── routers
├── services
├── repositories
├── schemas
├── models
├── handlers
├── exceptions
├── database
└── main.py
```

---

## Architecture

```text
Client
    │
    ▼
Router
    │
    ▼
Service
    │
    ▼
OpenAI Agent
    │
    ▼
Tool
    │
    ▼
Repository
    │
    ▼
Database / Knowledge
```

---

## Agent Workflow

```text
User Request
      │
      ▼
OpenAI Agent
      │
      ├── Task Tool
      ├── Search Document Tool
      ├── DateTime Tool
      ▼
Structured Output
      ▼
FastAPI Response
```

---

## Implemented Concepts

### Tool Calling

The Agent automatically selects appropriate tools based on user requests.

---

### Multi-step Tool Calling

The Agent can execute multiple tools in sequence.

Example:

```
Create a task and then list all tasks.
```

↓

```
create_task()

↓

get_tasks()
```

---

### Structured Output

The Agent returns strongly typed responses using Pydantic models.

Example:

```json
{
    "answer": "...",
    "source": "search_document"
}
```

---

### Session Context

Each request contains a session id allowing the Agent to maintain conversation state.

---

### Memory

Conversation history is preserved during the session.

---

### Simple RAG

Instead of answering only from the model knowledge, the Agent retrieves relevant documents before generating answers.

Workflow:

```
Question

↓

Search Document

↓

Retrieved Context

↓

LLM

↓

Answer
```

---

## Error Handling

- AIServiceError
- TaskNotFoundError
- TaskAlreadyExistsError
- TaskTitleEmptyError

Global Exception Handlers are implemented.

---

## Logging

Important operations are logged.

Examples:

- Tool execution
- Agent execution
- Exception logging

---

## API

### POST /chat

Chat with the AI Agent.

Request

```json
{
    "session_id": "demo",
    "message": "What is RAG?"
}
```

Response

```json
{
    "answer": "RAG combines retrieval and generation.",
    "source": "search_document"
}
```

---

## Future Improvements

- Vector Database
- Embedding Search
- Streaming Response
- Multi-Agent Architecture
- Guardrails
- MCP Integration

---

## Learning Outcomes

Through this project I learned:

- Building AI applications using OpenAI Agents SDK
- Designing AI tools with clear responsibilities
- Writing effective Agent Instructions
- Using Tool Docstrings to guide LLM behavior
- Implementing Structured Output with Pydantic
- Understanding Tool Calling and Multi-step Tool Calling
- Building a Simple RAG workflow
- Managing conversation context and memory
- Applying layered architecture (Router / Service / Repository)
- Implementing exception handling and logging