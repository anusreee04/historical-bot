from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Character(models.Model):
    name = models.CharField(max_length=100, unique=True)
    era = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    persona = models.TextField(blank=True)  # This defines how the AI should behave
    birth_date = models.CharField(max_length=50, blank=True)
    death_date = models.CharField(max_length=50, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    occupation = models.CharField(max_length=200, blank=True)
    major_achievements = models.TextField(blank=True)
    historical_context = models.TextField(blank=True)
    famous_quotes = models.TextField(blank=True)
    auto_generated = models.BooleanField(default=False)  # Track if info was auto-generated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class ChatHistory(models.Model):
    character_name = models.CharField(max_length=100)
    user_question = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
