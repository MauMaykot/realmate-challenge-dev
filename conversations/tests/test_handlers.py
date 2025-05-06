import uuid

from django.test import TestCase
from conversations.models import Conversation
from conversations.api.dispatcher import dispatch_event

class EventHandlerTests(TestCase):

  def test_new_conversation_event(self):
    conversation_id = uuid.uuid4()

    response_data = dispatch_event("NEW_CONVERSATION", { "id": str(conversation_id) })
    conversation  = response_data["conversation"]

    self.assertEqual(conversation_id, conversation.id)
    self.assertEqual("OPEN", Conversation.State.OPEN)
    self.assertEqual('Conversation created with success!', response_data["message"] )

    response_data = dispatch_event("NEW_CONVERSATION", { "id": str(conversation_id) })
    conversation  = response_data["conversation"]

    self.assertEqual(conversation_id, conversation.id)
    self.assertEqual("OPEN", Conversation.State.OPEN)
    self.assertEqual(f"Conversation with id: '{conversation_id}' already exists!", response_data["message"])