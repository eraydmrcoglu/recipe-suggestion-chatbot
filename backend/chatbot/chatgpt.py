from core.settings import OPENAI_API_KEY
import openai

openai.api_key = OPENAI_API_KEY


def get_chatbot_response(prompt: str) -> str:
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            temperature=0.9,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n", " Human:", " AI:"],
        )
    except Exception as error:
        return f"OpenAI API Error: {error}"

    return response.choices[0].text
