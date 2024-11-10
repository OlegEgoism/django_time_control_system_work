from django.urls import path, include, re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("<room_slug>", ChatConsumer.as_asgi()),
    path("ws/<str:room_slug>/", ChatConsumer.as_asgi()),
    path('ws/<room_slug>/', ChatConsumer.as_asgi()),
]

