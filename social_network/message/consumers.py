import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async
from .models import PrivateMessage, GroupMessageMember
from .serializers import PrivateMessageDetailSerializer, GroupMessageDetailSerializer

class PrivateMessageConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.message_id = self.scope['url_route']['kwargs']['message_id']
        self.message_group_name = f'message_{self.message_id}'
        self.user_id = self.scope["user"]
        try:
            self.private_message = await sync_to_async(PrivateMessage.objects.get, thread_sensitive=True)(pk=self.message_id)
            await sync_to_async(print, thread_sensitive=True)(self.private_message)
            if self.user_id not in (self.private_message.user_source, self.private_message.user_target):
                await self.close()
        except ObjectDoesNotExist:
            await self.close()
            
        await self.channel_layer.group_add(self.message_group_name, self.channel_name)
        await self.accept()
            
    async def receive(self, text_data):
        response = json.loads(text_data)
        message = response.get("message", None)
        
        data = await sync_to_async(self.create_message, thread_sensitive=True)(message)
        await self.channel_layer.group_send(self.message_group_name, {
            'type': 'send_message',
            'payload': data,
        })
        
    def create_message(self, message):
        data = {
            'message_id': self.message_id,
            'user_id': self.user_id.id,
            'content': message
        }
        serializer = PrivateMessageDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
            
    async def send_message(self, res):
        res['payload']['cuser'] = self.user_id.id
        await self.send(text_data=json.dumps(res))
            
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.message_group_name, self.channel_name)
        
    
class GroupMessageConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.message_id = self.scope['url_route']['kwargs']['message_id']
        self.message_group_name = f'message_group_{self.message_id}'
        self.user_id = self.scope["user"]
        try:
            self.group_message = await sync_to_async(GroupMessageMember.objects.filter, thread_sensitive=True)(group_message_id=self.message_id)
            valid_user = await sync_to_async(self.is_member, thread_sensitive=True)()
                
            if not valid_user:
                await self.close()
                    
        except ObjectDoesNotExist:
            await self.close()
            
        await self.channel_layer.group_add(self.message_group_name, self.channel_name)
        await self.accept()
            
    async def receive(self, text_data):
        response = json.loads(text_data)
        message = response.get("message", None)
        
        data = await sync_to_async(self.create_message, thread_sensitive=True)(message)
        await self.channel_layer.group_send(self.message_group_name, {
            'type': 'send_message',
            'payload': data,
        })
        
    def is_member(self):
        self.group_message = GroupMessageMember.objects.filter(group_message_id=self.message_id)
        valid_user = False
        for group in self.group_message:
            if self.user_id == group.user_id:
                valid_user = True
                break
        return valid_user
        
    def create_message(self, message):
        data = {
            'group_message_id': self.message_id,
            'user_id': self.user_id.id,
            'content': message
        }
        serializer = GroupMessageDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
            
    async def send_message(self, res):
        res['payload']['cuser'] = self.user_id.id
        await self.send(text_data=json.dumps(res))
            
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.message_group_name, self.channel_name)