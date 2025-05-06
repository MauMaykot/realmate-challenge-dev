from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('conversations.api.urls')),

    path('', include('conversations.urls')),
    path('', include('users.urls')),
]
