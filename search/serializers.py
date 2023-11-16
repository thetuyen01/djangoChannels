from rest_framework import serializers
from accounts.models import UserNTFriend

class UserNTFriendSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserNTFriend
        fields = '__all__'