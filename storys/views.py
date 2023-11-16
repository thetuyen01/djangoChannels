from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status    
from .models import Story
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserNTFriend
from news.models import Follow
from .serializers import StorySerializer, PostStorySerializer
from aiokafka import AIOKafkaProducer
import asyncio, json

class StoryAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    async def send_message_to_kafka(self, message_data, my_topic):
        producer = AIOKafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await producer.start()
        await producer.send_and_wait(my_topic, value=message_data)
        await producer.stop()


    def get(self, request):
        userntfrienf = UserNTFriend.objects.get(user = request.user.id)
        user = UserNTFriend.objects.get(id=userntfrienf.id)
        following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)

        # Lấy ra các bài story từ những người bạn đang theo dõi
        story_from_following = Story.objects.filter(author_id__in=following_users)

        # Sắp xếp bài viết theo thời gian đăng mới nhất
        story_from_following = story_from_following.order_by('-created_at')
        serializer = StorySerializer(story_from_following, many= True)
        return Response({
            "data":serializer.data,
            "status":True
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data 
        userntfrienf = UserNTFriend.objects.get(user = request.user.id)
        following_users = Follow.objects.filter(following=userntfrienf).values_list('follower', flat=True)
        data['author'] = userntfrienf.id
        serializer = PostStorySerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'messages': serializer.errors,
                'status': False
            },status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        story = StorySerializer(serializer.instance).data 
        story["list_user"] = list(following_users)
        asyncio.run(self.send_message_to_kafka(story, 'my_topic_story'))
        return Response({
            'message':'Add Story Succerfully',
            'status':True
        },status=status.HTTP_201_CREATED)
