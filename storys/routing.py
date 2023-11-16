from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/storys/(?P<id>\d+)/$', consumers.KafkaConsumerConsumer.as_asgi()),
]