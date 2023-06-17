import pytest
from chatbot import views


def test_chatbot_view_post_no_prompt(client):
    response = client.post("/chatgpt/")
    assert response.status_code == 400
    assert response.data == "No prompt provided"


def test_chatbot_view_post_no_session_id(client, openai_mock):
    openai_mock.return_value = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Hello!",
                },
            }
        ],
    }

    response = client.post("/chatgpt/", {"prompt": "Hello"})
    assert response.status_code == 200
    assert response.cookies["session_id"]
    assert response.data == "Hello!"


@pytest.mark.skip(reason="TODO: Fix this test")
def test_chatbot_view_post_with_session_id(client, openai_mock, monkeypatch):
    # Add session_id to CHATS to simulate a previous chat history
    monkeypatch.setitem(views.CHATS, "123", [])

    openai_mock.return_value = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Hello!",
                },
            }
        ],
    }

    client.cookies.load({"session_id": "123"})
    response = client.post(
        "/chatgpt/",
        {
            "prompt": "Hello",
        },
    )
    assert response.status_code == 200
    assert response.data == "Hello!"
    assert response.cookies["session_id"] == "123"
    assert views.CHATS["123"] == [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hello!"},
    ]


def test_chatbot_view_post_with_session_id_and_chat_history(client, openai_mock, monkeypatch):
    # Add session_id to CHATS to simulate a previous chat history
    monkeypatch.setitem(views.CHATS, "123", [{"role": "user", "content": "Hello 1"}])

    openai_mock.return_value = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Hello!",
                },
            }
        ],
    }

    response = client.post(
        "/chatgpt/",
        {
            "prompt": "Hello 2",
        },
        headers={"Cookie": "session_id=123"},
    )
    assert response.status_code == 200
    assert response.data == "Hello!"
    assert views.CHATS["123"] == [
        {"role": "user", "content": "Hello 1"},
        {"role": "user", "content": "Hello 2"},
        {"role": "assistant", "content": "Hello!"},
    ]


def test_chatbot_view_post_with_session_id_and_openai_api_error(client, openai_mock):
    openai_mock.side_effect = Exception("You have exceeded your API request rate limit.")

    response = client.post(
        "/chatgpt/",
        {
            "prompt": "Hello 2",
        },
    )
    assert response.status_code == 500
    assert response.data == "OpenAI API Error: You have exceeded your API request rate limit."
