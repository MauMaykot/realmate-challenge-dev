from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .dispatcher import dispatch_event

from conversations.models import Conversation
from conversations.api.serializers import ConversationSerializer

from django_filters.rest_framework import DjangoFilterBackend

class ConversationViewSet(ReadOnlyModelViewSet):
  queryset         = Conversation.objects.all().order_by("-id")
  serializer_class = ConversationSerializer
  lookup_field     = "id"
  filter_backends  = [DjangoFilterBackend]
  filterset_fields = ["state"]

@api_view(['POST'])
def webhook_view(request):
  try:

    event_type = request.data.get("type")
    if not event_type:
      raise Exception("Missing event_type")

    data = request.data.get("data")
    if not data:
      raise Exception("Missing data")

    timestamp = request.data.get("timestamp")
    if timestamp:
      data["timestamp"] = timestamp

    response_data = dispatch_event(event_type, data)
    response_data.pop('conversation', None)
    response_data.pop('message_object', None)

    return Response(response_data, status=status.HTTP_200_OK)

  except ValueError as ve:
    return Response({ "message": str(ve) }, status=status.HTTP_400_BAD_REQUEST)

  except Exception as e:
    return Response({ "message": str(e) }, status=status.HTTP_400_BAD_REQUEST)