from django.urls import reverse, resolve
from chatbot.views import ChatbotView


def test_urls():
    """Test django urls if they are working"""
    path = reverse("chatbot")
    assert resolve(path).view_name == "chatbot"
    assert resolve(path).func.__name__ == ChatbotView.as_view().__name__
