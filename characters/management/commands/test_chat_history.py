from django.core.management.base import BaseCommand
from characters.models import ChatHistory

class Command(BaseCommand):
    help = 'Test and display chat history from the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testing Chat History Database'))
        self.stdout.write('=' * 50)
        
        # Get all chat history records
        chat_history = ChatHistory.objects.all().order_by('-timestamp')
        total_count = chat_history.count()
        
        self.stdout.write(f'Total chat history records: {total_count}')
        
        if total_count == 0:
            self.stdout.write(self.style.WARNING('No chat history found in database.'))
            self.stdout.write('Try using the web interface to send a message first.')
        else:
            self.stdout.write(self.style.SUCCESS(f'Found {total_count} chat history records:'))
            self.stdout.write('')
            
            # Display the most recent 5 records
            for i, chat in enumerate(chat_history[:5], 1):
                self.stdout.write(f'{i}. Character: {chat.character_name}')
                self.stdout.write(f'   User: {chat.user_question[:100]}...' if len(chat.user_question) > 100 else f'   User: {chat.user_question}')
                self.stdout.write(f'   Bot: {chat.bot_response[:100]}...' if len(chat.bot_response) > 100 else f'   Bot: {chat.bot_response}')
                self.stdout.write(f'   Time: {chat.timestamp}')
                self.stdout.write('')
        
        # Test creating a sample record
        self.stdout.write('Creating a test chat history record...')
        test_chat = ChatHistory.objects.create(
            character_name='Test Character',
            user_question='This is a test question',
            bot_response='This is a test response'
        )
        
        self.stdout.write(self.style.SUCCESS(f'✅ Test record created with ID: {test_chat.id}'))
        
        # Verify the record was created
        new_count = ChatHistory.objects.count()
        self.stdout.write(f'New total count: {new_count}')
        
        if new_count > total_count:
            self.stdout.write(self.style.SUCCESS('✅ Database is working correctly!'))
        else:
            self.stdout.write(self.style.ERROR('❌ Database write test failed!'))
