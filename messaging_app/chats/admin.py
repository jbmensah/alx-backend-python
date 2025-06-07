from django.contrib import admin
from .models import CustomUser, Conversation, Message
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_group', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'created_at', 'is_read')
