import uuid

from chatbot.chatgpt import get_chatbot_response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

CHATS: dict[str, list[dict[str, str]]] = {}


def generate_session_id():
    session_id = uuid.uuid4().hex
    CHATS[session_id] = []
    return session_id


def get_session_chat_history(session_id):
    return CHATS.get(session_id, [])


class ChatbotView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_200_OK)

        prompt = request.data.get("prompt")
        if not prompt:
            return Response("No prompt provided", status=status.HTTP_400_BAD_REQUEST)

        chat_history = []
        if session_id := request.COOKIES.get("session_id"):
            chat_history = get_session_chat_history(session_id)
        else:
            session_id = generate_session_id()
            response.set_cookie("session_id", session_id)

        chat_history.append({"role": "user", "content": prompt})
        chatbot_response = get_chatbot_response(chat_history=chat_history)

        if "OpenAI API Error" in chatbot_response:
            return Response(
                chatbot_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        CHATS[session_id].append({"role": "user", "content": prompt})
        CHATS[session_id].append({"role": "assistant", "content": chatbot_response})

        response["Access-Control-Allow-Credentials"] = "true"
        response.data = chatbot_response

        return response
