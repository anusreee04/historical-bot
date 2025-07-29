# characters/urls.py
from django.urls import path
from .views import ChatWithCharacterView, index

print("Loading characters/urls.py")  # Debug print

urlpatterns = [
    path('', index, name='home'),          # Handles /
    path('chat/', ChatWithCharacterView.as_view(), name='chat'),  # Handles /api/chat/
]


