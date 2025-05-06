from django.urls import path

from .views import dash, chat

urlpatterns = [
  path("dash/", dash, name="dash"),
  path("chat/<uuid:conversation_id>/", chat, name="chat"),
]
