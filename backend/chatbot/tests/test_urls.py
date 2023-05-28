from chatbot.views import ChatbotView
from django.urls import resolve, reverse


def test_urls():
    """Test django urls if they are working"""
    path = reverse("chatbot")
    assert resolve(path).view_name == "chatbot"
    assert resolve(path).func.__name__ == ChatbotView.as_view().__name__
