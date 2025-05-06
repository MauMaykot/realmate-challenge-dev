from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .dispatcher import dispatch_event

@api_view(['POST'])
def webhook_view(request):
  try:

    event_type = request.data.get("type")
    if not event_type:
      return Response({ "message": "Missing event_type" }, status=status.HTTP_400_BAD_REQUEST)

    data = request.data.get("data")
    if not data:
      return Response({ "message": "Missing data" }, status=status.HTTP_400_BAD_REQUEST)

    timestamp = request.data.get("timestamp")
    if timestamp:
      data["timestamp"] = timestamp

    response_data = dispatch_event(event_type, data)

    status_code = response_data["status"]

    response_data.pop('status', None)
    response_data.pop('conversation', None)

    return Response(response_data, status=status_code)

  except ValueError as ve:
    return Response({ "message": str(ve) }, status=status.HTTP_400_BAD_REQUEST)

  except Exception as e:
    return Response({ "message": str(e) }, status=status.HTTP_400_BAD_REQUEST)