# -*- coding: utf-8 -*-
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from apps.display.routing import display_urlpatterns
# from apps.home.routing import home_urlpatterns

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(display_urlpatterns),
        # URLRouter(apps.home.routing.websocket_urlpatterns),
    ),
})
