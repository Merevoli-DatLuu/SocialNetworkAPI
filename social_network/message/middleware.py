from django.contrib.auth.models import AnonymousUser
import jwt
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from social_network.settings import SIMPLE_JWT, SECRET_KEY
from user.models import User


@database_sync_to_async
def get_user(token_key):
    try:
        user_id = jwt.decode(token_key, SECRET_KEY, algorithms=[SIMPLE_JWT['ALGORITHM']]).get(SIMPLE_JWT['USER_ID_CLAIM'])
    except jwt.exceptions.DecodeError:
        return AnonymousUser()
    except jwt.exceptions.ExpiredSignatureError:
        return AnonymousUser()
    try:
        return AnonymousUser() if user_id is None else User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = AnonymousUser() if token_key is None else await get_user(token_key)
        return await super().__call__(scope, receive, send)