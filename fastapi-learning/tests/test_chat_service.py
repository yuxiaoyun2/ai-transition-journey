from services import chat_service
from config import SYSTEM_PROMPT


rows = [(1, "hello", "hi", "...")]


def test_build_messages():
    messages = chat_service.build_messages(SYSTEM_PROMPT, rows)

    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "hello"
    assert messages[2]["role"] == "assistant"
    assert messages[2]["content"] == "hi"
