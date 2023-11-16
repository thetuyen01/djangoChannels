from django.urls import path
from .views import VideoAPIView

urlpatterns = [
    path('videoshorts/', VideoAPIView.as_view(), name='video'),
]