from django.urls import path
from .views import ChatGroupAPIView, ChatMessageAPIView

urlpatterns = [
    path('chatmessage/<int:user>', ChatMessageAPIView.as_view(), name='message'),
    path('chatgroup/', ChatGroupAPIView.as_view(), name='group')
]