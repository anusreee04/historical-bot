"""
Services for fetching and generating character information
"""
import requests
import json
import re
import os
from groq import Groq


class CharacterInfoService:
    """Service for fetching and generating character information"""
    
    @staticmethod
    def fetch_wikipedia_info(character_name):
        """Fetch character information from Wikipedia API"""
        try:
            # Search for the character on Wikipedia
            search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{character_name.replace(' ', '_')}"
            
            response = requests.get(search_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                info = {}
                
                # Extract basic information
                if 'extract' in data:
                    info['description'] = data['extract'][:1500]  # Limit to 1500 chars
                
                # Try to extract birth/death dates from the extract
                extract = data.get('extract', '')
                if extract:
                    # Simple regex extraction for dates
                    date_pattern = r'(\d{1,2}\s+\w+\s+\d{4}|\d{4})'
                    dates = re.findall(date_pattern, extract)
                    if len(dates) >= 2:
                        info['birth_date'] = dates[0]
                        info['death_date'] = dates[1]
                        info['era'] = f"{dates[0]}-{dates[1]}"
                    elif len(dates) == 1:
                        info['birth_date'] = dates[0]
                        info['era'] = dates[0]
                
                # Extract additional info from the extract
                if extract:
                    # Try to identify nationality
                    nationality_patterns = [
                        r'(\w+)\s+(?:physicist|scientist|leader|politician|artist|writer|philosopher)',
                        r'born\s+in\s+(\w+)',
                        r'(\w+)\s+independence',
                        r'(\w+)\s+revolutionary'
                    ]
                    
                    for pattern in nationality_patterns:
                        match = re.search(pattern, extract, re.IGNORECASE)
                        if match:
                            info['nationality'] = match.group(1)
                            break
                    
                    # Try to identify occupation
                    occupation_patterns = [
                        r'was\s+an?\s+([^.]+?)(?:\s+who|\s+and|\.|,)',
                        r'is\s+an?\s+([^.]+?)(?:\s+who|\s+and|\.|,)',
                    ]
                    
                    for pattern in occupation_patterns:
                        match = re.search(pattern, extract, re.IGNORECASE)
                        if match:
                            occupation = match.group(1).strip()
                            if len(occupation) < 100:  # Reasonable length
                                info['occupation'] = occupation
                            break
                
                return info
                
        except Exception as e:
            print(f"Error fetching Wikipedia info: {e}")
            return {}
        
        return {}

    @staticmethod
    def generate_persona_with_ai(character_info):
        """Generate an authentic persona using AI based on character information"""
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            
            # Create a comprehensive prompt for persona generation
            prompt = f"""
            Create an authentic persona for {character_info.get('name', 'this historical figure')} based on the following information:
            
            Name: {character_info.get('name', 'Unknown')}
            Era: {character_info.get('era', 'Unknown')}
            Birth: {character_info.get('birth_date', 'Unknown')}
            Death: {character_info.get('death_date', 'Unknown')}
            Nationality: {character_info.get('nationality', 'Unknown')}
            Occupation: {character_info.get('occupation', 'Unknown')}
            Description: {character_info.get('description', 'No description available')}
            Major Achievements: {character_info.get('major_achievements', 'Unknown')}
            
            Create a detailed persona that includes:
            1. How they should speak (tone, vocabulary, phrases they might use)
            2. Key topics they would discuss
            3. Their philosophical views and beliefs
            4. Important events from their life they might reference
            5. Their personality traits and mannerisms
            6. Historical context of their time period
            
            Format this as a single paragraph that can be used as a system prompt for an AI chatbot to roleplay as this character authentically.
            Start with "You are {character_info.get('name', 'this historical figure')}..." and make it comprehensive but concise (under 600 words).
            Include specific historical details, speaking patterns, and personality traits that would make the character feel authentic.
            """
            
            chat_completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are an expert historian and character analyst. Create authentic personas for historical figures based on historical facts and documented personality traits."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            generated_persona = chat_completion.choices[0].message.content
            return generated_persona
            
        except Exception as e:
            print(f"Error generating persona: {e}")
            return None

    @staticmethod
    def generate_additional_details(character_info):
        """Generate additional historical details using AI"""
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            
            prompt = f"""
            Based on the historical figure {character_info.get('name', 'Unknown')}, provide the following information in a structured format:
            
            Known information:
            - Name: {character_info.get('name', 'Unknown')}
            - Era: {character_info.get('era', 'Unknown')}
            - Description: {character_info.get('description', 'No description')}
            
            Please provide:
            1. Major Achievements (3-5 key accomplishments)
            2. Historical Context (the time period and world events during their life)
            3. Famous Quotes (2-3 authentic quotes if known, otherwise indicate "No documented quotes available")
            
            Format your response as:
            MAJOR_ACHIEVEMENTS: [list the achievements]
            HISTORICAL_CONTEXT: [describe the historical context]
            FAMOUS_QUOTES: [list quotes or indicate none available]
            
            Be historically accurate and only include verified information.
            """
            
            chat_completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are a professional historian. Provide accurate historical information."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=600
            )
            
            response = chat_completion.choices[0].message.content
            
            # Parse the response
            details = {}
            if "MAJOR_ACHIEVEMENTS:" in response:
                achievements = response.split("MAJOR_ACHIEVEMENTS:")[1].split("HISTORICAL_CONTEXT:")[0].strip()
                details['major_achievements'] = achievements
            
            if "HISTORICAL_CONTEXT:" in response:
                context = response.split("HISTORICAL_CONTEXT:")[1].split("FAMOUS_QUOTES:")[0].strip()
                details['historical_context'] = context
            
            if "FAMOUS_QUOTES:" in response:
                quotes = response.split("FAMOUS_QUOTES:")[1].strip()
                details['famous_quotes'] = quotes
            
            return details
            
        except Exception as e:
            print(f"Error generating additional details: {e}")
            return {}

    @classmethod
    def auto_populate_character(cls, character):
        """Automatically populate character information from various sources"""
        from .models import Character
        
        success = False
        
        # Fetch basic info from Wikipedia
        wiki_info = cls.fetch_wikipedia_info(character.name)
        if wiki_info:
            # Update character with Wikipedia info
            for key, value in wiki_info.items():
                if hasattr(character, key) and value:
                    setattr(character, key, value)
            success = True
        
        # Generate additional details with AI
        character_info = {
            'name': character.name,
            'era': character.era,
            'birth_date': character.birth_date,
            'death_date': character.death_date,
            'nationality': character.nationality,
            'occupation': character.occupation,
            'description': character.description,
            'major_achievements': character.major_achievements,
        }
        
        # Generate AI persona
        persona = cls.generate_persona_with_ai(character_info)
        if persona:
            character.persona = persona
            character.auto_generated = True
            success = True
        
        # Generate additional details
        additional_details = cls.generate_additional_details(character_info)
        if additional_details:
            for key, value in additional_details.items():
                if hasattr(character, key) and value:
                    setattr(character, key, value)
            success = True
        
        return success
