"""
ASGI config for ecommerce project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
from django.urls import path
from shop.consumers import *
application = get_asgi_application()

ws_patterns = [
   path('ws/test/<order_id>',TestConsumer),
   path('ws/test2/<username>',NotificationConsumer)

]

application = ProtocolTypeRouter({
  "websocket":URLRouter(ws_patterns) 
  # Just HTTP for now. (We can add other protocols later.)
})