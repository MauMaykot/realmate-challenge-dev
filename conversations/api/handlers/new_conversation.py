import uuid

from conversations.models import Conversation

from rest_framework import status

def handle(data):

  id = data["id"]
  if not id:
    return { "message": "Missing id", "status": status.HTTP_400_BAD_REQUEST }

  id = uuid.UUID(id)
  conversation, created = Conversation.objects.get_or_create(id=id, defaults={ "state": Conversation.State.OPEN })

  if created:
    message = "Conversation created with success!"
  else:
    message = f"Conversation with id: '{conversation.id}' already exists!"

  response_data = {
    "conversation": conversation,
    "message": message,
    "status": status.HTTP_200_OK
  }

  return response_data