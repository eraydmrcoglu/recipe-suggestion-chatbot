import logging
import uuid

from chatbot.chatgpt import DEFAULT_PROMPT, get_chatbot_response
from chatbot.utils import set_cookie
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

CHATS: dict[str, list[dict[str, str]]] = {}
logging.basicConfig(level=logging.INFO)


def generate_session_id():
    session_id = uuid.uuid4().hex
    CHATS[session_id] = DEFAULT_PROMPT
    return session_id


def get_session_chat_history(session_id):
    if history := CHATS.get(session_id, []):
        return history
    else:
        logging.info(f"No chat history found for session_id: {session_id}")
        return []


class ChatbotView(APIView):
    def post(self, request):
        session_id = request.COOKIES.get("session_id", None)
        response = Response(status=status.HTTP_200_OK)

        prompt = request.data.get("prompt")
        if not prompt:
            return Response("No prompt provided", status=status.HTTP_400_BAD_REQUEST)

        chat_history = []

        if session_id:
            logging.info(f"Request session_id cookie: {session_id}")
            chat_history = get_session_chat_history(session_id)
            if not chat_history:
                session_id = generate_session_id()
                set_cookie(response, "session_id", session_id)
                CHATS[session_id].append({"role": "user", "content": prompt})
        else:
            logging.info("No session_id cookie found, generating new session_id")
            session_id = generate_session_id()
            logging.info(f"Generated session_id: {session_id}")
            set_cookie(response, "session_id", session_id)
            CHATS[session_id].append({"role": "user", "content": prompt})

        chat_history.append({"role": "user", "content": prompt})

        chatbot_response = get_chatbot_response(chat_history=chat_history)
        # chatbot_response = "This is a test"

        if "OpenAI API Error" in chatbot_response:
            return Response(chatbot_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        CHATS[session_id].append({"role": "assistant", "content": chatbot_response})

        response.data = chatbot_response

        return response
