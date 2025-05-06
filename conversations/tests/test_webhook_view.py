import uuid

from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from conversations.models import Conversation

class WebhookViewTest(APITestCase):

    def setUp(self):
      self.url = reverse("webhook")

    def test_should_return_error_if_missing_data(self):
      payload = { "type": None }

      response = self.client.post(self.url, data=payload, format='json')
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

      data = response.data
      message = data["message"]
      self.assertEqual('Missing event_type', message)

      payload = {
        "type": "NEW_CONVERSATION",
        "data": {}
      }

      response = self.client.post(self.url, data=payload, format='json')
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

      data = response.data
      message = data["message"]
      self.assertEqual('Missing data', message)

      payload = {
        "type": "NEW_CONVERSATION",
        "data": { "id": "" }
      }

      response = self.client.post(self.url, data=payload, format='json')
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

      data = response.data
      message = data["message"]
      self.assertEqual('Missing id', message)

    def test_new_conversation_via_post(self):
      conversation_id = uuid.uuid4()

      payload = {
        "type": "NEW_CONVERSATION",
        "data": {
          "id": str(conversation_id)
        }
      }

      response = self.client.post(self.url, data=payload, format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)

      data = response.data

      message = data["message"]
      self.assertEqual('Conversation created with success!', message)

      conversation = Conversation.objects.get(id=conversation_id)
      self.assertEqual(conversation.state, Conversation.State.OPEN)

      response = self.client.post(self.url, data=payload, format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)

      data = response.data
      message = data["message"]
      self.assertEqual(f"Conversation with id: '{conversation_id}' already exists!", message)
