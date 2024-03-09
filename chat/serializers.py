from rest_framework import serializers
from .models import Conversation, Message



class ConversationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Conversation
        fields = ['id', 'user', 'label', 'last_message', 'created_at',  'updated_at']

class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ['query', 'response', 'created_at']
