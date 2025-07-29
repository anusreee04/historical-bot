from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from groq import Groq
import os
from django.shortcuts import render
from .models import ChatHistory, Character

def index(request):
    return render(request, 'index.html')

# Helper function to get character from database
def get_character_by_name(name):
    """Get character from database by name (case-insensitive)"""
    try:
        return Character.objects.get(name__iexact=name)
    except Character.DoesNotExist:
        return None

def get_available_characters():
    """Get all available characters from database"""
    return Character.objects.all()

class ChatWithCharacterView(APIView):
    def post(self, request, *args, **kwargs):
        user_message = request.data.get("message")
        character_name = request.data.get("character", "").strip()

        if not user_message:
            return Response({"error": "No message provided."}, status=status.HTTP_400_BAD_REQUEST)

        if not character_name:
            return Response({"error": "No character specified."}, status=status.HTTP_400_BAD_REQUEST)

        # Get character from database
        character = get_character_by_name(character_name)
        if not character:
            return Response({"error": f"Character '{character_name}' not found. Available characters: {[c.name for c in get_available_characters()]}"}, status=status.HTTP_400_BAD_REQUEST)

        # Use the character's persona as the system prompt
        system_prompt = character.persona

        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            chat_completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            reply = chat_completion.choices[0].message.content

            # Save chat history to database
            ChatHistory.objects.create(
                character_name=character.name,
                user_question=user_message,
                bot_response=reply
            )

            return Response({
                "character": character.name,
                "reply": reply
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class ChatHistoryView(APIView):
    def get(self, request, *args, **kwargs):
        """Get chat history, optionally filtered by character"""
        character_name = request.query_params.get('character')

        if character_name:
            chat_history = ChatHistory.objects.filter(
                character_name__icontains=character_name
            ).order_by('-timestamp')
        else:
            chat_history = ChatHistory.objects.all().order_by('-timestamp')

        # Limit to last 50 conversations to avoid overwhelming response
        chat_history = chat_history[:50]

        history_data = []
        for chat in chat_history:
            history_data.append({
                'id': chat.id,
                'character_name': chat.character_name,
                'user_question': chat.user_question,
                'bot_response': chat.bot_response,
                'timestamp': chat.timestamp.isoformat()
            })

        return Response({
            'chat_history': history_data,
            'total_count': len(history_data)
        })


class CharactersListView(APIView):
    def get(self, request, *args, **kwargs):
        """Get list of all available characters"""
        characters = Character.objects.all().order_by('name')

        characters_data = []
        for character in characters:
            characters_data.append({
                'id': character.id,
                'name': character.name,
                'era': character.era,
                'description': character.description
            })

        return Response({
            'characters': characters_data,
            'total_count': len(characters_data)
        })
