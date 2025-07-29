

# Register your models here.
from django.contrib import admin
from .models import Character, ChatHistory
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages

# Try to import the service, but handle gracefully if dependencies are missing
try:
    from .services import CharacterInfoService
    SERVICES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: CharacterInfoService not available: {e}")
    SERVICES_AVAILABLE = False
    CharacterInfoService = None


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'era', 'nationality', 'occupation', 'auto_generated_status', 'created_at')
    list_filter = ('era', 'nationality', 'auto_generated', 'created_at')
    search_fields = ('name', 'era', 'description', 'nationality', 'occupation')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at', 'auto_generated')

    # Organize fields into sections
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'era', 'birth_date', 'death_date')
        }),
        ('Background', {
            'fields': ('nationality', 'occupation', 'description')
        }),
        ('AI Persona & Details', {
            'fields': ('persona', 'major_achievements', 'historical_context', 'famous_quotes'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('auto_generated', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def auto_generated_status(self, obj):
        """Show if character info was auto-generated"""
        if obj.auto_generated:
            return format_html('<span style="color: green;">✓ Auto-generated</span>')
        else:
            return format_html('<span style="color: orange;">✋ Manual</span>')
    auto_generated_status.short_description = "Info Source"

    # Custom actions
    actions = ['duplicate_character', 'auto_populate_character_info', 'regenerate_persona']

    def duplicate_character(self, request, queryset):
        """Action to duplicate selected characters"""
        for character in queryset:
            character.pk = None  # This will create a new instance
            character.name = f"{character.name} (Copy)"
            character.save()
        self.message_user(request, f"Successfully duplicated {queryset.count()} character(s).")
    duplicate_character.short_description = "Duplicate selected characters"

    def auto_populate_character_info(self, request, queryset):
        """Action to auto-populate character information using APIs"""
        if not SERVICES_AVAILABLE:
            messages.error(request, "Auto-population service is not available. Please install required dependencies (requests, groq).")
            return

        success_count = 0
        error_count = 0

        for character in queryset:
            try:
                if CharacterInfoService.auto_populate_character(character):
                    character.save()
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                error_count += 1
                messages.error(request, f"Error processing {character.name}: {str(e)}")

        if success_count > 0:
            messages.success(request, f"Successfully auto-populated {success_count} character(s).")
        if error_count > 0:
            messages.warning(request, f"Failed to process {error_count} character(s).")

    auto_populate_character_info.short_description = "🤖 Auto-populate character details from APIs"

    def regenerate_persona(self, request, queryset):
        """Action to regenerate AI persona for selected characters"""
        if not SERVICES_AVAILABLE:
            messages.error(request, "Persona generation service is not available. Please install required dependencies (requests, groq).")
            return

        success_count = 0
        error_count = 0

        for character in queryset:
            try:
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

                persona = CharacterInfoService.generate_persona_with_ai(character_info)
                if persona:
                    character.persona = persona
                    character.auto_generated = True
                    character.save()
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                error_count += 1
                messages.error(request, f"Error regenerating persona for {character.name}: {str(e)}")

        if success_count > 0:
            messages.success(request, f"Successfully regenerated persona for {success_count} character(s).")
        if error_count > 0:
            messages.warning(request, f"Failed to regenerate persona for {error_count} character(s).")

    regenerate_persona.short_description = "🎭 Regenerate AI persona"

    def save_model(self, request, obj, form, change):
        """Override save to auto-populate new characters"""
        is_new = not obj.pk

        # Save the object first
        super().save_model(request, obj, form, change)

        # If it's a new character and most fields are empty, try to auto-populate
        if is_new and not obj.description and not obj.persona and SERVICES_AVAILABLE:
            try:
                if CharacterInfoService.auto_populate_character(obj):
                    obj.save()
                    messages.success(request, f"✨ Auto-populated details for {obj.name} using Wikipedia and AI!")
                else:
                    messages.info(request, f"Could not auto-populate details for {obj.name}. You can use the 'Auto-populate' action later.")
            except Exception as e:
                messages.warning(request, f"Error auto-populating {obj.name}: {str(e)}")
        elif is_new and not SERVICES_AVAILABLE:
            messages.info(request, f"Auto-population service not available. You can manually fill in the details for {obj.name}.")


@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('character_name', 'user_question_preview', 'bot_response_preview', 'timestamp')
    list_filter = ('character_name', 'timestamp')
    search_fields = ('character_name', 'user_question', 'bot_response')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

    def user_question_preview(self, obj):
        """Show a preview of the user question"""
        if len(obj.user_question) > 50:
            return obj.user_question[:50] + "..."
        return obj.user_question
    user_question_preview.short_description = "User Question"

    def bot_response_preview(self, obj):
        """Show a preview of the bot response"""
        if len(obj.bot_response) > 50:
            return obj.bot_response[:50] + "..."
        return obj.bot_response
    bot_response_preview.short_description = "Bot Response"

    # Custom actions
    actions = ['delete_selected_chats']

    def delete_selected_chats(self, request, queryset):
        """Action to delete selected chat history"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Successfully deleted {count} chat history record(s).")
    delete_selected_chats.short_description = "Delete selected chat history"


# Customize admin site headers
admin.site.site_header = "Historical Characters Admin"
admin.site.site_title = "Historical Characters Admin Portal"
admin.site.index_title = "Welcome to Historical Characters Administration"



