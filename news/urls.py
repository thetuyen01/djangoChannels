from django.urls import path
from .views import NewsPostAPIView, FollowAIPView, CommentsAPIView

urlpatterns = [
    path('tin/', NewsPostAPIView.as_view(), name='tin'),
    path('follow/', FollowAIPView.as_view(), name='follow'),
    path('comment/', CommentsAPIView.as_view(), name='comment')
]