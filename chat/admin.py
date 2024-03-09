from django.contrib import admin
from .models import *

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1 

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'user', 'user', 'created_at' )
    inlines = [MessageInline]

admin.site.register(Conversation, ConversationAdmin)


