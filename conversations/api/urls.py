from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import webhook_view, ConversationViewSet

router = DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")

urlpatterns = [
  path("webhook/", webhook_view, name="webhook"),

  path("", include(router.urls)),
]
