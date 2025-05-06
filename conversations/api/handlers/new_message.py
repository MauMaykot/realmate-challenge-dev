import uuid

from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from conversations.models import Conversation, Message

def handle(data):

  conversation_id = data["conversation_id"]
  if not conversation_id:
    raise Exception("Missing conversation_id")

  conversation_id = uuid.UUID(conversation_id)

  message_id = data["id"]
  if not message_id:
    raise Exception("Missing message_id")

  message_id = uuid.UUID(message_id)

  conversation = get_object_or_404(Conversation, pk=conversation_id)
  if conversation.state == Conversation.State.CLOSED:
    raise Exception("This conversation is closed")

  timestamp = data.get('timestamp')
  if timestamp:
    timestamp = parse_datetime(timestamp)
  else:
    timestamp = timezone.now()

  message, created = Message.objects.get_or_create(
    id           = message_id,
    direction    = data.get("direction"),
    content      = data.get("content"),
    timestamp    = timestamp,
    conversation = conversation
  )

  if not created:
    raise Exception(f"Cannot create message with same id: '{message_id}'")

  response_data = {
    "conversation": conversation,
    "message_object": message,
    "message": "Message created with success!",
  }

  return response_data