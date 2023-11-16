from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/newspost/(?P<id>\d+)/$', consumers.KafkaConsumerConsumer.as_asgi()),
    re_path(r'ws/commentnotify/(?P<id>\d+)/$', consumers.KafkaConsumerConsumerCommetNotifile.as_asgi()),
    re_path(r'ws/addcomments/(?P<id>\d+)/$', consumers.sendAddPostKafkaConsumerConsumer.as_asgi())
]