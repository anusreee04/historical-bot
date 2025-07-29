#!/usr/bin/env python
"""
Test the API functionality for character auto-population
This script tests the Wikipedia and AI integration independently
"""

import requests
import json
import re
import os
from groq import Groq

def test_wikipedia_api(character_name):
    """Test Wikipedia API for character information"""
    print(f"📚 Testing Wikipedia API for: {character_name}")
    print("-" * 40)
    
    try:
        # Search for the character on Wikipedia
        search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{character_name.replace(' ', '_')}"
        
        response = requests.get(search_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Wikipedia API successful!")
            print(f"Title: {data.get('title', 'N/A')}")
            print(f"Extract: {data.get('extract', 'N/A')[:200]}...")
            
            # Try to extract dates
            extract = data.get('extract', '')
            if extract:
                date_pattern = r'(\d{1,2}\s+\w+\s+\d{4}|\d{4})'
                dates = re.findall(date_pattern, extract)
                if dates:
                    print(f"Dates found: {dates}")
            
            return data
        else:
            print(f"❌ Wikipedia API failed with status: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_groq_api(character_info):
    """Test Groq AI API for persona generation"""
    print(f"\n🤖 Testing Groq AI API for persona generation")
    print("-" * 40)
    
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        if not os.getenv("GROQ_API_KEY"):
            print("❌ GROQ_API_KEY not found in environment variables")
            return None
        
        prompt = f"""
        Create an authentic persona for {character_info.get('name', 'this historical figure')} based on the following information:
        
        Name: {character_info.get('name', 'Unknown')}
        Description: {character_info.get('description', 'No description available')[:500]}
        
        Create a detailed persona that includes how they should speak, key topics they would discuss, and their personality traits.
        Format this as a system prompt for an AI chatbot. Start with "You are [Name]..." and keep it under 300 words.
        """
        
        chat_completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are an expert historian. Create authentic personas for historical figures."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )
        
        persona = chat_completion.choices[0].message.content
        print("✅ Groq AI API successful!")
        print(f"Generated persona: {persona[:200]}...")
        
        return persona
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Main test function"""
    print("🧪 API Functionality Test")
    print("=" * 50)
    
    # Test with a famous historical figure
    character_name = "Winston Churchill"
    
    # Test Wikipedia API
    wiki_data = test_wikipedia_api(character_name)
    
    if wiki_data:
        # Test Groq AI API
        character_info = {
            'name': character_name,
            'description': wiki_data.get('extract', '')
        }
        
        persona = test_groq_api(character_info)
        
        if persona:
            print("\n🎉 Both APIs working successfully!")
            print("\nThis means the admin can:")
            print("1. ✅ Add a character name")
            print("2. ✅ Auto-fetch Wikipedia information")
            print("3. ✅ Generate AI persona")
            print("4. ✅ Create authentic chatbot character")
        else:
            print("\n⚠️ Wikipedia works, but AI generation failed")
    else:
        print("\n❌ Wikipedia API test failed")
    
    print("\n" + "=" * 50)
    print("Test complete!")

if __name__ == "__main__":
    main()
