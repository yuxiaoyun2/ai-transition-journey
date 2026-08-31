from unittest.mock import MagicMock
from app.services.ai_service import AIService
from app.core.config import Settings


def test_ai_service():
    mock_client = MagicMock()
    settings = MagicMock(spec=Settings)
    settings.openai_chat_model = "test-chat-model"

    mock_message = MagicMock()
    mock_message.content = "ai answer"

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    mock_client = mock_client.return_value
    mock_client.chat.completions.create.return_value = mock_response

    ai_client = AIService(client=mock_client, settings=settings)

    prompt = "test openai response"

    result = ai_client.generate_chat(prompt=prompt)

    assert result == "ai answer"

    mock_client.chat.completions.create.assert_called_once_with(
        model=settings.openai_chat_model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
