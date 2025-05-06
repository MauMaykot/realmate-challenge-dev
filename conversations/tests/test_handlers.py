import uuid

from django.test import TestCase
from conversations.models import Conversation, Message
from conversations.api.dispatcher import dispatch_event

class EventHandlerTests(TestCase):

  def test_new_conversation_event(self):
    conversation_id = uuid.uuid4()

    response_data = dispatch_event("NEW_CONVERSATION", { "id": str(conversation_id) })
    conversation  = response_data["conversation"]

    self.assertEqual(conversation_id, conversation.id)
    self.assertEqual("OPEN", Conversation.State.OPEN)
    self.assertEqual('Conversation created with success!', response_data["message"] )

    with self.assertRaisesMessage(Exception, f"Conversation with id: '{conversation_id}' already exists!"):
      dispatch_event("NEW_CONVERSATION", { "id": str(conversation_id) })

  def test_new_message_event(self):
    conversation_id = uuid.uuid4()

    conversation = Conversation.objects.create(id=conversation_id, state=Conversation.State.OPEN)

    for direction, _ in Message.Direction.choices:
      message_id = uuid.uuid4()

      event_data = {
        "id": str(message_id),
        "direction": direction,
        "content": f"Mensagem de teste {direction}",
        "conversation_id": str(conversation_id)
      }

      dispatch_event("NEW_MESSAGE", event_data)

      message = Message.objects.get(id=message_id)
      self.assertEqual(direction, message.direction)
      self.assertEqual(f"Mensagem de teste {direction}", message.content)
      self.assertEqual(conversation_id, message.conversation.id)

    conversation.state = Conversation.State.CLOSED
    conversation.save()

    message_id = uuid.uuid4()
    event_data = {
      "id": str(message_id),
      "direction": "SENT",
      "content": "Mensagem de teste",
      "conversation_id": str(conversation_id)
    }

    with self.assertRaisesMessage(Exception, "This conversation is closed"):
      dispatch_event("NEW_MESSAGE", event_data)