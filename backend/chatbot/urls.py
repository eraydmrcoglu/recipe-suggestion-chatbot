from django.urls import path
from chatbot import views

urlpatterns = [
    path("", views.ChatbotView.as_view(), name="chatbot"),
]
