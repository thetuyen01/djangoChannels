from django.urls import path
from . import views


urlpatterns = [
    path('storys/', views.StoryAPIView.as_view(), name='StoryAPIView'),
]