# backend/urls.py
from django.contrib import admin
from django.urls import path
from characters.views import ChatWithCharacterView, ChatHistoryView, CharactersListView, index

print("Loading backend/urls.py")  # Debug print

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chat/', ChatWithCharacterView.as_view(), name='chat'),  # Direct mapping
    path('api/chat-history/', ChatHistoryView.as_view(), name='chat-history'),  # Chat history endpoint
    path('api/characters/', CharactersListView.as_view(), name='characters-list'),  # Characters list endpoint
    path('', index, name='home'),
    path('', index, name='index'),# Direct mapping for root
]

