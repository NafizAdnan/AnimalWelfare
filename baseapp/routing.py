from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:support_name>/',consumers.ChatConsumer.as_asgi()),
]