import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


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




