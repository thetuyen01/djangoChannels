from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status    
from django.db.models import Q
from accounts.models import UserNTFriend
from .serializers import UserNTFriendSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class GetProfileUserNTFriendView(APIView):
    def get(self, request, id_user):
        try:
            userntfriend = get_object_or_404(UserNTFriend, id=id_user)
            serializer = UserNTFriendSerializer(userntfriend)
            return Response({
                "data": serializer.data,
                "status": True
            })
        except Exception as e:
            return Response({
                "status": str(e),
                "code": 500
            })

class GetAllProfileUserNTFriendView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            userntfriends = UserNTFriend.objects.all()
            if request.user.id:
                userntfriends = UserNTFriend.objects.exclude(user=request.user.id)
    
            if request.GET.get('search') :
                search = request.GET.get('search')
                userntfriends = UserNTFriend.objects.filter(Q(id__icontains = search)|Q(name__exact=search)|Q(name__icontains=search))

            if request.GET.get('limit'):
                limit = request.GET.get('limit')
                userntfriends = UserNTFriend.objects.filter(Q(id__icontains = limit)|Q(name__exact=limit)|Q(name__icontains=limit))[:6]

            serializer = UserNTFriendSerializer(userntfriends, many=True)
            return Response({
                "data": serializer.data,
                "status": True
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": str(e),
                "code": 500
            }, status=status.HTTP_400_BAD_REQUEST)
