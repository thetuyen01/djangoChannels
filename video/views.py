from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserNTFriend
from .models import *
from .serializers import VideoSerializer, PostVideoSerializer

class VideoAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many = True)
        return Response({
            "data":serializer.data,
            "status":True
        }, status=status.HTTP_200_OK)
    

    def post(self, request):
        data = request.data
        userntfriend = UserNTFriend.objects.filter(user = request.user.id).first()
        data['user'] = userntfriend.id
        serializer = PostVideoSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'messages':serializer.errors,
                'status': False
            },status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({
            "data":serializer.data,
            "status":True
        }, status=status.HTTP_200_OK)