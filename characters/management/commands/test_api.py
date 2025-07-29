from django.core.management.base import BaseCommand
from django.test import Client
import json

class Command(BaseCommand):
    help = 'Test the chat history API endpoint'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testing Chat History API'))
        self.stdout.write('=' * 50)
        
        # Create a test client
        client = Client()
        
        # Test the chat history API endpoint
        try:
            response = client.get('/api/chat-history/')
            
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('✅ Chat History API is working!'))
                
                data = response.json()
                total_count = data.get('total_count', 0)
                chat_history = data.get('chat_history', [])
                
                self.stdout.write(f'Total records returned: {total_count}')
                
                if chat_history:
                    self.stdout.write('\nRecent chat history from API:')
                    for i, chat in enumerate(chat_history[:3], 1):
                        self.stdout.write(f'{i}. {chat["character_name"]}: {chat["user_question"][:50]}...')
                        self.stdout.write(f'   Response: {chat["bot_response"][:50]}...')
                        self.stdout.write(f'   Time: {chat["timestamp"]}')
                        self.stdout.write('')
                else:
                    self.stdout.write('No chat history returned from API')
                    
            else:
                self.stdout.write(self.style.ERROR(f'❌ API call failed with status: {response.status_code}'))
                self.stdout.write(f'Response: {response.content.decode()}')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error testing API: {str(e)}'))
        
        # Test filtering by character
        try:
            self.stdout.write('\nTesting character filtering...')
            response = client.get('/api/chat-history/?character=gandhi')
            
            if response.status_code == 200:
                data = response.json()
                filtered_count = data.get('total_count', 0)
                self.stdout.write(self.style.SUCCESS(f'✅ Character filtering works! Found {filtered_count} Gandhi records'))
            else:
                self.stdout.write(self.style.ERROR('❌ Character filtering failed'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error testing character filtering: {str(e)}'))
