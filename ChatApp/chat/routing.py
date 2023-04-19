# Import required modules
from django.urls import path, include, re_path
from chat.consumers import ChatConsumer

# Define a list of WebSocket URL patterns
websocket_urlpatterns = [
    # An empty path means that any WebSocket connection will be handled by the ChatConsumer
    path("", ChatConsumer.as_asgi()),
    # A path with the regex pattern "ws/chat/<room_name>" means that WebSocket connections
    # to this URL with a room name will be handled by the ChatConsumer
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]