import openai
from core.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

DEFAULT_PROMPT = [
    {
        "role": "user",
        "content": 'I want you to act as a food recipe guide. You are here to help answer any questions I may have about the food recipe. Please note that if my question is not related to food recipe, you have to write only "Error". Let\'s get started.',  # noqa
    },
    {
        "role": "assistant",
        "content": "Sure, I'm here to help you with any food recipe-related questions you have! What would you like to know?",  # noqa
    },
]


def get_chatbot_response(chat_history: list[dict[str, str]]) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=DEFAULT_PROMPT + chat_history,
        )
    except Exception as error:
        return f"OpenAI API Error: {error}"

    return response.choices[0]["message"]["content"]
