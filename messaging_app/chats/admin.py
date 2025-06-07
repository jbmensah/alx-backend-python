import uuid
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Conversation, Message

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Show these columns in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    # Allow searching by these fields
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    # Fields to display when editing a user
    fieldsets = (
        (None, {'fields': ('user_id','username','password')}),
        ('Personal info', {'fields': ('first_name','last_name','email','bio','avatar','phone_number')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Important dates', {'fields': ('last_login','date_joined')}),
    )
    # Fields to display when creating a user via the admin “Add user” form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','password1','password2','is_staff','is_active'),
        }),
    )

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'is_group', 'name', 'created_at')
    filter_horizontal = ('participants',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'conversation', 'sender', 'sent_at', 'is_read')
    list_filter = ('is_read', 'sent_at')
    search_fields = ('message_body', 'sender__username')
