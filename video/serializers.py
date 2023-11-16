from rest_framework import serializers
from .models import *
from accounts.models import UserNTFriend

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNTFriend
        fields = ['id', 'name', 'image']  # Thêm trường 'age' vào danh sách các trường cần hiển thị


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Like
        fields = ['id', 'user', 'video']

class CommentsVideoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = CommentVideo
        fields = ['user', 'video', 'content', 'created_at']


class VideoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()  # Sử dụng CommentSerializer để serialize danh sách bình luận
    class Meta:
        model  = Video
        fields = ['id', 'description', 'video_url', 'user', 'likes', 'comments']

    def get_likes(self, obj):
        likes = Like.objects.filter(video=obj) 
        return LikeSerializer(likes, many=True).data
    
    def get_comments(self, obj):
        comments = CommentVideo.objects.filter(video=obj)  # Lấy tất cả bình luận liên quan đến bài viết (post)
        return CommentsVideoSerializer(comments, many=True).data



class PostVideoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = '__all__'