import uuid

from conversations.models import Conversation

from django.shortcuts import get_object_or_404

def handle(data):

  id = data["id"]
  if not id:
    raise Exception("Missing id")

  id = uuid.UUID(id)
  conversation = get_object_or_404(Conversation, id=id)

  if conversation.is_closed():
    raise Exception("This conversation is already closed!")

  conversation.state = Conversation.State.CLOSED
  conversation.save()

  response_data = {
    "conversation": conversation,
    "message": "Conversation closed with success!",
  }

  return response_data