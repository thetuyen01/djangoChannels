from django.urls import path
from . import views


urlpatterns = [
    path('userntfriend/', views.GetAllProfileUserNTFriendView.as_view(), name='GetAllProfileUserNTFriendView'),
    path('profile/<int:id_user>/', views.GetProfileUserNTFriendView.as_view(), name='GetProfileUserNTFriendView'),
]