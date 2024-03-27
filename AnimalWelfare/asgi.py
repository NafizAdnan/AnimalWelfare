import os
import django
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.auth import AuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter

import support.routing



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AnimalWelfare.settings')
django.setup()



application = ProtocolTypeRouter({
    "http":get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            support.routing.websocket_urlpatterns
        )
    )
})