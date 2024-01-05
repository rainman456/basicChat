import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer



from django.template.loader import get_template


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
       
        self.room_group_name="anita"
       
        name=self.channel_name
        await self.channel_layer.group_add(
            self.room_group_name,name)
        await self.accept()
        #await self.send(text_data=json.dumps(name))
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender=text_data_json['sender']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender':sender
            }
        )
        print(message)
        print(sender)
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        outgoing=event['sender']
        #message_html = f"<div hx-swap-oob='beforeend:#messages'><p  id='message'>{message}</p></div>"
        await self.send(text_data=json.dumps( {"message": message,"username":outgoing }))
       








