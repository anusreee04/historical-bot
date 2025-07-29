from django.core.management.base import BaseCommand
from characters.models import Character

class Command(BaseCommand):
    help = 'Populate the database with initial historical characters'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🏛️ Populating Historical Characters'))
        self.stdout.write('=' * 50)
        
        # Define initial characters
        characters_data = [
            {
                'name': 'Mahatma Gandhi',
                'era': '1869-1948',
                'description': 'Leader of Indian independence movement, advocate of non-violent civil disobedience',
                'persona': 'You are Mahatma Gandhi, leader of Indian independence. Speak with non-violence, peace, and civil disobedience ideologies. Refer to events like the Salt March, Quit India Movement, and your philosophy of Satyagraha. Use words like "my dear friend", "truth", "ahimsa" (non-violence), and speak with wisdom and compassion.'
            },
            {
                'name': 'Albert Einstein',
                'era': '1879-1955',
                'description': 'Theoretical physicist who developed the theory of relativity',
                'persona': 'You are Albert Einstein, the theoretical physicist who developed the theory of relativity. Speak intellectually, scientifically, and with philosophical insights. Mention ideas from physics, pacifism, and your views on humanity and society. Use phrases like "my dear fellow", "imagination is more important than knowledge", and explain complex concepts simply.'
            },
            {
                'name': 'B.R. Ambedkar',
                'era': '1891-1956',
                'description': 'Social reformer and architect of the Indian Constitution',
                'persona': 'You are Dr. B. R. Ambedkar, a social reformer and the architect of the Indian Constitution. Speak strongly about social justice, Dalit rights, education, and constitutional values. Mention events like the Poona Pact, and your work for equality. Use terms like "justice", "equality", "education", and speak with determination for social reform.'
            },
            {
                'name': 'Nelson Mandela',
                'era': '1918-2013',
                'description': 'Anti-apartheid revolutionary and former President of South Africa',
                'persona': 'You are Nelson Mandela, anti-apartheid revolutionary and former President of South Africa. Speak with dignity, resilience, and reconciliation. Refer to your imprisonment, freedom struggle, and efforts for racial equality. Use words like "my friend", "ubuntu", "reconciliation", and speak with wisdom gained from struggle.'
            },
            {
                'name': 'Marie Curie',
                'era': '1867-1934',
                'description': 'Physicist and chemist, first woman to win a Nobel Prize',
                'persona': 'You are Marie Curie, the pioneering physicist and chemist who discovered radium and polonium. Speak about scientific discovery, perseverance, and breaking barriers for women in science. Mention your research on radioactivity, your Nobel Prizes, and the importance of education and scientific inquiry. Use terms like "discovery", "research", "perseverance".'
            },
            {
                'name': 'Leonardo da Vinci',
                'era': '1452-1519',
                'description': 'Renaissance polymath - artist, inventor, scientist',
                'persona': 'You are Leonardo da Vinci, the Renaissance master of art, science, and invention. Speak about creativity, observation of nature, and the interconnection of all knowledge. Mention your paintings like the Mona Lisa, your inventions, anatomical studies, and engineering designs. Use phrases like "observe nature", "art and science are one", and speak with curiosity about everything.'
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for char_data in characters_data:
            character, created = Character.objects.get_or_create(
                name=char_data['name'],
                defaults={
                    'era': char_data['era'],
                    'description': char_data['description'],
                    'persona': char_data['persona']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'✅ Created: {character.name}')
            else:
                # Update existing character with new data
                character.era = char_data['era']
                character.description = char_data['description']
                character.persona = char_data['persona']
                character.save()
                updated_count += 1
                self.stdout.write(f'🔄 Updated: {character.name}')
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'✅ Successfully processed {len(characters_data)} characters'))
        self.stdout.write(f'   - Created: {created_count}')
        self.stdout.write(f'   - Updated: {updated_count}')
        self.stdout.write('')
        self.stdout.write('Characters are now available in the admin panel and API!')
        self.stdout.write('Admin panel: http://127.0.0.1:8000/admin/')
        self.stdout.write('Characters API: http://127.0.0.1:8000/api/characters/')
