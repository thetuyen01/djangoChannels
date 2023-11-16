from rest_framework import serializers
from .models import *
from accounts.models import UserNTFriend

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Post
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNTFriend
        fields = ['id', 'name', 'image']  # Thêm trường 'age' vào danh sách các trường cần hiển thị

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model  = Comment
        fields = ['post', 'text', 'user', 'created']

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Comment
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Follow
        fields = '__all__'


class NewsGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    comments = CommentSerializer(many=True)  # Sử dụng CommentSerializer để serialize danh sách bình luận
    class Meta:
        model  = Post
        fields = ['id', 'picture', 'caption', 'posted', 'tag', 'user', 'likes', 'comments']

    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj)  # Lấy tất cả bình luận liên quan đến bài viết (post)
        return CommentSerializer(comments, many=True).data
