from urllib import parse
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

from django.db import close_old_connections
from django.conf import settings
import jwt
from django.contrib.auth import get_user_model



@database_sync_to_async
def get_user(user_id):

    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        #Delay imports unitl app registry is complete
        from django.contrib.auth.models import AnonymousUser
        return AnonymousUser()

class JwtCustomMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        #Delay imports until app registry is complete
        from django.contrib.auth.models import AnonymousUser
        from rest_framework_simplejwt.tokens import UntypedToken
        from rest_framework_simplejwt.exceptions import TokenError, InvalidToken



        close_old_connections()

        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")
        user = AnonymousUser()

        if token:
            try:
                UntypedToken(token[0])

                data = jwt.decode(token[0], settings.SECRET_KEY, algorithms=["HS256"])
                user_id = data.get("user_id")
                if user_id:
                    user = await get_user(user_id)

            except (InvalidToken, TokenError, jwt.DecodeError):
                pass

        scope["user"] = user
        return await super().__call__(scope,receive,send)

