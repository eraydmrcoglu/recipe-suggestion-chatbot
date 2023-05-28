from unittest.mock import patch

from chatbot import chatgpt


def test_get_chatbot_response(openai_mock):
    chat_history = [
        {
            "role": "user",
            "content": "Hello, can you help me with a recipe?",
        },
    ]

    openai_mock.return_value = {
        "id": "chatcmpl-6p9XYPYSTTRi0xEviKjjilqrWU2Ve",
        "object": "chat.completion",
        "created": 1677649420,
        "model": "gpt-3.5-turbo",
        "usage": {"prompt_tokens": 56, "completion_tokens": 31, "total_tokens": 87},
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Sure, I'm here to help you with any food recipe-related questions you have!",
                },
                "finish_reason": "stop",
                "index": 0,
            }
        ],
    }

    response = chatgpt.get_chatbot_response(chat_history)
    assert response == "Sure, I'm here to help you with any food recipe-related questions you have!"


@patch("chatbot.chatgpt.openai.ChatCompletion.create")
def test_get_chatbot_response_exception(mock_chatbot_response):
    mock_chatbot_response.side_effect = Exception("You have exceeded your API usage")

    response = chatgpt.get_chatbot_response([])

    assert response == "OpenAI API Error: You have exceeded your API usage"
