from django.urls import path

from .views import user_login

urlpatterns = [
  path("accounts/login/", user_login, name="login"),
]
