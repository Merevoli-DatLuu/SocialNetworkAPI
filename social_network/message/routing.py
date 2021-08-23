from django.urls import path

from .consumers import PrivateMessageConsumer, GroupMessageConsumer

ws_urlpatterns = [
    path('ws/message/<message_id>', PrivateMessageConsumer.as_asgi()),
    path('ws/message/group/<message_id>', GroupMessageConsumer.as_asgi())
]
