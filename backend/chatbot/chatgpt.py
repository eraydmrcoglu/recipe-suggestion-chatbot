import openai
from core.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def get_chatbot_response(chat_history: list[dict[str, str]]) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )
    except Exception as error:
        return f"OpenAI API Error: {error}"

    return response.choices[0]["message"]["content"]
