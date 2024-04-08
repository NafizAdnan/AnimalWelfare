import os
import django
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

# from chat.routing 
# import baseapp.routing
# from notification_app.routing import websocket_urlpatterns

#from channels.auth import AuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns
from baseapp.routing import websocket_urlpatterns as baseapp_websocket_urlpatterns
from notification_app.routing import websocket_urlpatterns as notification_websocket_urlpatterns




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AnimalWelfare.settings')
django.setup()

websocket_urlpatterns = (
    chat_websocket_urlpatterns +
    baseapp_websocket_urlpatterns +
    notification_websocket_urlpatterns
)
 

application = ProtocolTypeRouter({
    "http":get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})

 

# application = ProtocolTypeRouter({
#     "http":get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     )
# })