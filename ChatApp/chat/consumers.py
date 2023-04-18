import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Get the user's interests
#         user = self.scope['user']
#         interests = user.interests.split(',')

#         # Find another online user with similar interests
#         match = None
#         for interest in interests:
#             matches = User.objects.filter(is_online=True, interests__contains=interest).exclude(pk=user.pk)
#             if matches.exists():
#                 match = matches.first()
#                 break

#         # If no match found, connect with a random online user
#         if match is None:
#             matches = User.objects.filter(is_online=True).exclude(pk=user.pk)
#             if matches.exists():
#                 match = matches.first()

#         if match is not None:
#             # Set both users as offline
#             user.is_online = False
#             user.save()
#             match.is_online = False
#             match.save()

#             # Connect the two users
#             self.user_1 = user
#             self.user_2 = match
#             self.room_name = f'chat_{self.user_1.pk}_{self.user_2.pk}'
#             self.room_group_name = f'chat_{self.user_1.pk}_{self.user_2.pk}'
#             await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#             await self.accept()
#             await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'message': 'You are now connected.'})
#         else:
#             await self.close()

#     async def disconnect(self, close_code):
#         if hasattr(self, 'room_group_name'):
#             await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'message': 'The other user has disconnected.'})
#             await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
#             self.user_1.is_online = True
#             self.user_1.save()
#             self.user_2.is_online = True
#             self.user_2.save()

#     async def receive(self, text_data):
#         message = json.loads(text_data)['message']
#         await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'message': message})

#     async def chat_message(self, event):
#         message = event['message']
#         await self.send(text_data=json.dumps({'message': message}))