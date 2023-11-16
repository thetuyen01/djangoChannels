from rest_framework import serializers
from .models import Story
from accounts.models import UserNTFriend
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNTFriend
        fields = ['id', 'name', 'image']  # Thêm trường 'age' vào danh sách các trường cần hiển thị

class StorySerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Story
        fields = ['id', 'title', 'created_at', 'image', 'video_url', 'author']

class PostStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'
