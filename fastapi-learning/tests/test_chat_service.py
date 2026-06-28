from services import chat_service
from config import SYSTEM_PROMPT
from unittest.mock import patch, Mock
import unittest

rows = [(1, "hello", "hi", "...")]


def test_build_messages():
    messages = chat_service.build_messages(SYSTEM_PROMPT, rows)

    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "hello"
    assert messages[2]["role"] == "assistant"
    assert messages[2]["content"] == "hi"


@patch("services.chat_service.client.chat.completions.create")
@patch("services.chat_service.get_recent_chat_rows")
@patch("services.chat_service.save_chat_message")
def test_generate_answer(
    mock_save_chat_message, mock_get_recent_chat_rows, mock_create
):
    mock_resp = Mock()
    mock_choice = Mock()
    mock_message = Mock()
    mock_message.content = "open ai answer"
    mock_choice.message = mock_message
    mock_resp.choices = [mock_choice]

    mock_create.return_value = mock_resp
    mock_get_recent_chat_rows.return_value = []

    answer = chat_service.generate_answer("hello")

    assert answer == "open ai answer"

    mock_create.assert_called_once()

    mock_save_chat_message.assert_called_once_with(
        user_message="hello", ai_answer="open ai answer"
    )
