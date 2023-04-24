from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatbot.chatgpt import get_chatbot_response


class ChatbotView(APIView):
    def post(self, request):
        prompt = request.data.get("prompt")
        if not prompt:
            return Response("No prompt provided", status=status.HTTP_400_BAD_REQUEST)

        chatbot_response = get_chatbot_response(prompt)

        if "OpenAI API Error" in chatbot_response:
            return Response(chatbot_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(chatbot_response, status=status.HTTP_200_OK)
