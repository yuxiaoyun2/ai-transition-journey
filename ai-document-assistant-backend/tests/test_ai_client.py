from unittest.mock import patch, MagicMock
from app.ai.ai_client import AIClient
from app.config import OPENAI_MODEL, SUMMARY_PROMPT, OPENAI_API_KEY, PROMPT
from app.exceptions.custom_exceptions import AIServiceError

from openai import OpenAIError
import pytest


@patch("app.ai.ai_client.OpenAI")
def test_generate_summary(mock_openai):

    mock_message = MagicMock
    mock_message.content = "ai answer"

    mock_choice = MagicMock
    mock_choice.message = mock_message

    mock_response = MagicMock
    mock_response.choices = [mock_choice]

    mock_client = mock_openai.return_value
    mock_client.chat.completions.create.return_value = mock_response

    ai_client = AIClient()
    input_text = "これはテスト用のドキュメントです。"

    result = ai_client.generate_summary(text=input_text)

    assert result == "ai answer"

    mock_openai.assert_called_once_with(api_key=OPENAI_API_KEY)

    mock_client.chat.completions.create.assert_called_once_with(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": SUMMARY_PROMPT,
            },
            {
                "role": "user",
                "content": input_text,
            },
        ],
    )


@patch("app.ai.ai_client.OpenAI")
def test_generate_summary_openai_error(mock_openai):
    # Arrange
    mock_client = mock_openai.return_value
    mock_client.chat.completions.create.side_effect = OpenAIError("OpenAI API errror")

    ai_client = AIClient()

    # Act & Assert
    with pytest.raises(AIServiceError):
        ai_client.generate_summary(text="テスト用ドキュメント")


@patch("app.ai.ai_client.OpenAI")
def test_generate_chat(mock_openai):
    message_mock = MagicMock()
    message_mock.content = "ai chat response"

    choice_mock = MagicMock()
    choice_mock.message = message_mock

    response_mock = MagicMock()
    response_mock.choices = [choice_mock]

    mock_client = mock_openai.return_value
    mock_client.chat.completions.create.return_value = response_mock

    ai_client = AIClient()

    doc_text = "テスト用ドキュメント"

    question = "テスト用クエスション"

    answer = ai_client.generate_chat(doc_text=doc_text, question=question)

    assert answer == "ai chat response"

    mock_openai.assert_called_once_with(api_key=OPENAI_API_KEY)

    expected_prompt = "Document:\n" f"{doc_text}\n\n" "Question:\n" f"{question}"
    mock_client.chat.completions.create.assert_called_once_with(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": PROMPT,
            },
            {
                "role": "user",
                "content": expected_prompt,
            },
        ],
    )


@patch("app.ai.ai_client.OpenAI")
def test_generate_chat_openai_error(mock_openai):
    mock_client = mock_openai.return_value
    mock_client.chat.completions.create.side_effect = OpenAIError("OpenAI API Error")

    ai_client = AIClient()

    text = "テスト用ドキュメント"

    question = "テスト用クエスション"

    with pytest.raises(AIServiceError):
        ai_client.generate_chat(doc_text=text, question=question)
