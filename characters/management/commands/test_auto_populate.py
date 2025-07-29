from django.core.management.base import BaseCommand
from characters.models import Character
from characters.services import CharacterInfoService

class Command(BaseCommand):
    help = 'Test the auto-population functionality for characters'

    def add_arguments(self, parser):
        parser.add_argument('character_name', type=str, help='Name of the character to test')

    def handle(self, *args, **options):
        character_name = options['character_name']
        
        self.stdout.write(self.style.SUCCESS(f'🧪 Testing Auto-Population for: {character_name}'))
        self.stdout.write('=' * 60)
        
        # Create a test character
        try:
            character, created = Character.objects.get_or_create(
                name=character_name,
                defaults={'description': '', 'persona': ''}
            )
            
            if created:
                self.stdout.write(f'✅ Created new character: {character_name}')
            else:
                self.stdout.write(f'📝 Using existing character: {character_name}')
                # Clear existing data for testing
                character.description = ''
                character.persona = ''
                character.era = ''
                character.birth_date = ''
                character.death_date = ''
                character.nationality = ''
                character.occupation = ''
                character.major_achievements = ''
                character.historical_context = ''
                character.famous_quotes = ''
                character.auto_generated = False
                character.save()
                self.stdout.write('🧹 Cleared existing data for testing')
            
            # Test Wikipedia API
            self.stdout.write('\n📚 Testing Wikipedia API...')
            wiki_info = CharacterInfoService.fetch_wikipedia_info(character_name)
            if wiki_info:
                self.stdout.write(self.style.SUCCESS('✅ Wikipedia API successful!'))
                for key, value in wiki_info.items():
                    self.stdout.write(f'  - {key}: {value[:100]}...' if len(str(value)) > 100 else f'  - {key}: {value}')
            else:
                self.stdout.write(self.style.WARNING('⚠️ Wikipedia API returned no data'))
            
            # Test AI persona generation
            self.stdout.write('\n🤖 Testing AI Persona Generation...')
            character_info = {
                'name': character_name,
                'era': wiki_info.get('era', ''),
                'birth_date': wiki_info.get('birth_date', ''),
                'death_date': wiki_info.get('death_date', ''),
                'nationality': wiki_info.get('nationality', ''),
                'occupation': wiki_info.get('occupation', ''),
                'description': wiki_info.get('description', ''),
                'major_achievements': '',
            }
            
            persona = CharacterInfoService.generate_persona_with_ai(character_info)
            if persona:
                self.stdout.write(self.style.SUCCESS('✅ AI Persona generation successful!'))
                self.stdout.write(f'Persona preview: {persona[:200]}...')
            else:
                self.stdout.write(self.style.WARNING('⚠️ AI Persona generation failed'))
            
            # Test additional details generation
            self.stdout.write('\n📖 Testing Additional Details Generation...')
            additional_details = CharacterInfoService.generate_additional_details(character_info)
            if additional_details:
                self.stdout.write(self.style.SUCCESS('✅ Additional details generation successful!'))
                for key, value in additional_details.items():
                    self.stdout.write(f'  - {key}: {value[:100]}...' if len(str(value)) > 100 else f'  - {key}: {value}')
            else:
                self.stdout.write(self.style.WARNING('⚠️ Additional details generation failed'))
            
            # Test full auto-population
            self.stdout.write('\n🚀 Testing Full Auto-Population...')
            success = CharacterInfoService.auto_populate_character(character)
            if success:
                character.save()
                self.stdout.write(self.style.SUCCESS('✅ Full auto-population successful!'))
                
                # Display final character info
                self.stdout.write('\n📋 Final Character Information:')
                self.stdout.write(f'Name: {character.name}')
                self.stdout.write(f'Era: {character.era}')
                self.stdout.write(f'Birth: {character.birth_date}')
                self.stdout.write(f'Death: {character.death_date}')
                self.stdout.write(f'Nationality: {character.nationality}')
                self.stdout.write(f'Occupation: {character.occupation}')
                self.stdout.write(f'Description: {character.description[:200]}...' if character.description else 'Description: (empty)')
                self.stdout.write(f'Persona: {character.persona[:200]}...' if character.persona else 'Persona: (empty)')
                self.stdout.write(f'Auto-generated: {character.auto_generated}')
                
            else:
                self.stdout.write(self.style.ERROR('❌ Full auto-population failed'))
            
            self.stdout.write('\n' + '=' * 60)
            if success:
                self.stdout.write(self.style.SUCCESS('🎉 Test completed successfully!'))
                self.stdout.write(f'You can now chat with {character_name} using the web interface.')
                self.stdout.write('Admin panel: http://127.0.0.1:8000/admin/characters/character/')
            else:
                self.stdout.write(self.style.ERROR('❌ Test failed. Check the error messages above.'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error during testing: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
