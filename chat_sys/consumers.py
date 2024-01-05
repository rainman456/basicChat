import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

#from django.utils.timesince import timesince
#from .utils import send_message_to_group
#from accounts.models import Account
#from .models import Room, Message
#from .templatetags.chatextras import initials

from django.template.loader import get_template


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #self.room_name = self.scope['url_route']['kwargs']['room_name']
        #self.room_group_name = f"chat_{self.room_name}"
        self.room_group_name="anita"
        # Join room group
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
       
"""   
    def get_message_style(self):
        style1=get_template("message_style1.html",).render(
            context={
                "messages": message
                
            }
        )

        # Alternate between two styles based on the message counter
        if self.message_counter % 2 == 0:
            self.message_counter += 1
            return style1
        else:
            self.message_counter += 1
            return style-2
        
        
"""
"""
async def chat_message(self, event):
    message = event['message']
    message_html_style1 = f"<div hx-swap-oob='beforeend:#messages' class='style-1'><p>{message}</p></div>"
    message_html_style2 = f"<div hx-swap-oob='beforeend:#messages' class='style-2'><p>{message}</p></div>"

    # Send messages with different styles to WebSocket
    await self.send(text_data=json.dumps({
        'message': message_html_style1
    }))

    await self.send(text_data=json.dumps({
        'message': message_html_style2
    }))




class ChatConsumer(AsyncWebsocketConsumer):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.message_counter = 0

    async def chat_message(self, event):
        message = event['message']
        message_html = f"<div hx-swap-oob='beforeend:#messages' class='{self.get_message_style()}'>{message}</div>"

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message_html
        }))

    def get_message_style(self):
        # Alternate between two styles based on the message counter
        if self.message_counter % 2 == 0:
            self.message_counter += 1
            return 'style-1'
        else:
            self.message_counter += 1
            return 'style-2'








"""