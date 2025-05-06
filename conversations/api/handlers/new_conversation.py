import uuid

from conversations.models import Conversation

def handle(data):

  id = data["id"]
  if not id:
    raise Exception("Missing id")

  id = uuid.UUID(id)
  conversation, created = Conversation.objects.get_or_create(id=id, defaults={ "state": Conversation.State.OPEN })

  if not created:
    raise Exception(f"Conversation with id: '{conversation.id}' already exists!")

  response_data = {
    "conversation": conversation,
    "message": "Conversation created with success!",
  }

  return response_data