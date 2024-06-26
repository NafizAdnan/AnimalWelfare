import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'notifications_%s' % self.scope["user"].id
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

    # Receive message from room group
    async def send_notification(self, event):
        message = event['message']
        url = event.get('url', '')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'url': url
        }))


class ChatConsumer( AsyncWebsocketConsumer):
   async def connect(self):
       self.support_name = self.scope['url_route']['kwargs']['support_name']
       self.support_group_name = 'chat_%s' % self.support_name

       await self.channel_layer.group_add(
           self.support_group_name,
           self.channel_name
       )
       await self.accept()

   async def disconnect(self):
       await self.channel_layer.group_discard(
           self.support_group_name,
           self.channel_name
       )

   async def receive(self,text_data):
       data = json.loads(text_data)
       message = data['message']
       username = data['username']
       support = data['support']

       await self.channel_layer.group_send(
           self.support_group_name,
           {
               'type' : 'chat_message',
               'message' : message,
               'username' : username,
               'support': support,
           }
       )

   async def chat_message(self,event):
       message = event['message']
       username = event['username']
       support = event['support']

       await self.send(text_data=json.dumps({
           'message' : message,
           'username' : username,
           'support': support,

       }))




