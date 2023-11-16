from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server/(?P<custom_string>[\w\s-]+)/$', consumers.KafkaConsumerConsumer.as_asgi()),
    re_path(r'ws/online/', consumers.OnlineStatusConsumer.as_asgi()),
    re_path(r'ws/notify/(?P<id>\d+)/$', consumers.NotificationConsumer.as_asgi())
]