from rest_framework import serializers
from .models import *
from accounts.models import UserNTFriend



class UserNTFriendSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserNTFriend
        fields = ['id','name','status','image','user']
    def get_status(self, obj):
        # Lấy trạng thái từ model UserStatus hoặc bất kỳ cách nào khác phù hợp với ứng dụng của bạn
        try:
            userntfriend = UserNTFriend.objects.get(pk=obj.id)
            user_status = UserProfileModel.objects.filter(user = userntfriend).first()
            if user_status:
                return str(user_status.online_status)
            else:
                return False
            
            
        except UserProfileModel.DoesNotExist:
            return False  # Mặc định là offline nếu không có dữ liệu trạng thái


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

class ChatGroupSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many= True)
    participants = UserNTFriendSerializer(many= True)
    class Meta:
        model = ChatGroup
        fields = ['chat_name','messages','participants']



