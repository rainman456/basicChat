"""
ASGI config for freindsapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_basic.settings")
asgi_application = get_asgi_application()

import chat_sys.routing
application = ProtocolTypeRouter(
    {
        'http': asgi_application,
        'websocket': AllowedHostsOriginValidator(URLRouter(chat_sys.routing.websocket_urlpatterns)),
    }
)

