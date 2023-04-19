import json
from channels.generic.websocket import AsyncWebsocketConsumer

# Define a consumer that handles WebSocket connections
class ChatConsumer(AsyncWebsocketConsumer):
    
    # Runs when a client connects to the WebSocket
    async def connect(self):
        # Get the room name from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # Create a group name for this room
        self.room_group_name = 'chat_%s' % self.room_name

        # Add the client's channel to the room's channel group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the connection
        await self.accept()

    # Runs when a client disconnects from the WebSocket
    async def disconnect(self, close_code):
        # Remove the client's channel from the room's channel group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Runs when a client sends a message over the WebSocket
    async def receive(self, text_data):
        # Parse the message as JSON
        data = json.loads(text_data)
        # Extract the message and username from the JSON
        message = data['message']
        username = data['username']

        # Send the message to the room's channel group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive a message from the room's channel group
    async def chat_message(self, event):
        # Extract the message and username from the message event
        message = event['message']
        username = event['username']

        # Send the message to the client
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))