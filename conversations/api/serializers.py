from rest_framework import serializers
from conversations.models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Message
    fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
  messages = MessageSerializer(many=True)

  class Meta:
    model = Conversation
    fields = '__all__'