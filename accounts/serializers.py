from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import UserNTFriend
from chatapp.models import UserProfileModel

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        
        if data['email']:
            if User.objects.filter(email = data['email']).first():
                raise serializers.ValidationError("email da ton tai")
        
        if data['username']:
            if User.objects.filter(username = data['username']).first():
                raise serializers.ValidationError("username da ton tai")
            
        return data
    
    def create(self, validated_data):
        user = User.objects.create(email= validated_data['email'], username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        userntfriend = UserNTFriend.objects.create(user= user, name = user.username)
        userntfriend.save()
        userprofile = UserProfileModel.objects.create(user = userntfriend)
        userprofile.save()

        return validated_data
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    
    def get_jwt_token(self, data):
        user = authenticate(username = data['username'], password = data['password'])

        if not user:
            raise serializers.ValidationError({
                "message":"tai khoang mat khau khong dung",
                "status":False
            })
        
        refresh = RefreshToken.for_user(user)
        userntfirend = UserNTFriend.objects.filter(user=user).first()

        return {
            'refreshToken': str(refresh),
            'accessToken': str(refresh.access_token),
            'id_user':userntfirend.id,
            'status':True
        }
        
   
            