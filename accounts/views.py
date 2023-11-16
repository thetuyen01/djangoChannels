from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
# Create your views here.
class RegisterAPIView(APIView):

    def post(self, request):
        data= request.data
        serializer = RegisterSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "status":False,
                "message":"register that bai"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({
            "status":True,
            "message":"register thanh cong"
        }, status=status.HTTP_201_CREATED)
    
class LoginAPIView(APIView):

    def post(self, request):
        data = request.data 
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "status":False,
                "message":"login that bai"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        response = serializer.get_jwt_token(data=serializer.data)
        
        return Response({
            "data":response,
            "message":"login thanh cong"
        },status=status.HTTP_201_CREATED)