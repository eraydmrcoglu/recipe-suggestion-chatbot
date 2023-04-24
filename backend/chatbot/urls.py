from chatbot import views
from django.urls import path

urlpatterns = [
    path("", views.ChatbotView.as_view(), name="chatbot"),
]
