from django.urls import path

from .views import user_login, user_logout

urlpatterns = [
  path("accounts/login/", user_login, name="login"),
  path("accounts/logout/", user_logout, name="logout"),
]
