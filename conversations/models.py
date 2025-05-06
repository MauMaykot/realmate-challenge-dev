from django.utils.translation import gettext_lazy as _

from django.db import models

class Conversation(models.Model):

  class State(models.TextChoices):
    OPEN   = "OPEN", _("Open")
    CLOSED = "CLOSED", _("Closed")

  id    = models.UUIDField(primary_key=True)
  state = models.CharField(max_length=6, choices=State.choices, default=State.OPEN)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

  def is_closed(self):
    return self.state == self.__class__.State.CLOSED

class Message(models.Model):

  class Direction(models.TextChoices):
    SENT     = "SENT", _("Sent")
    RECEIVED = "RECEIVED", _("Received")

  id           = models.UUIDField(primary_key=True)
  conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
  direction    = models.CharField(max_length=8, choices=Direction.choices)
  content      = models.TextField()

  timestamp    = models.DateTimeField()