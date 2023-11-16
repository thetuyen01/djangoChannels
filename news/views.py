from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import PostSerializer,NewsGetSerializer, UserSerializer, PostCommentSerializer, FollowSerializer
from .models import *
from aiokafka import AIOKafkaProducer
import asyncio, json
from accounts.models import UserNTFriend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from uuid import UUID

class NewsPostAPIView(APIView):
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

        # Lấy ra các bài viết từ những người bạn đang theo dõi
        posts_from_following = Post.objects.filter(user__in=following_users)

        # Sắp xếp bài viết theo thời gian đăng mới nhất
        posts_from_following = posts_from_following.order_by('-posted')
        serializer = NewsGetSerializer(posts_from_following, many= True)
        return Response({
            "data":serializer.data,
            "status":True
        }, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data 
        userntfrienf = UserNTFriend.objects.get(user = request.user.id)
        following_users = Follow.objects.filter(following=userntfrienf).values_list('follower', flat=True)
        data['user']= userntfrienf.id
        serializer = PostSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'messages':'no value ',
                'status': False
            },status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        get_sz = NewsGetSerializer(serializer.instance).data
        get_sz["list_user"]=list(following_users)
        asyncio.run(self.send_message_to_kafka(get_sz, 'quickstart-events'))
        return Response({
            'message':'Add Post Succerfully',
            'status':True
        },status=status.HTTP_201_CREATED)
    

class FollowAIPView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id 
        userntfriend = UserNTFriend.objects.filter(user = user_id).first()
        users_not_followed = UserNTFriend.objects.exclude(id__in=Follow.objects.filter(follower=userntfriend).values('following')).exclude(id = userntfriend.id)
        serializer = UserSerializer(users_not_followed, many = True)
        return Response({
            "data":serializer.data,
            "status":True
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        print(data['other_id'])
        user_id = request.user.id 
        userntfriend = UserNTFriend.objects.filter(user = user_id).first()
        otheruserntfriend = UserNTFriend.objects.filter(id = int(data['other_id'])).first()
        data = {
            "follower":userntfriend.id,
            "following":otheruserntfriend.id
        }
        serializer = FollowSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'messages':serializer.errors,
                'status': False
            },status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({
            "messages":"Follow succerfully",
            "status":True
        }, status=status.HTTP_200_OK)
        


class CommentsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    async def send_message_to_kafka(self, message_data, my_topic):
        def uuid_encoder(obj):
            if isinstance(obj, UUID):
                return str(obj)
            raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

        producer = AIOKafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v, default=uuid_encoder).encode('utf-8')
        )
        await producer.start()
        await producer.send_and_wait(my_topic, value=message_data)
        await producer.stop()

    def post(self, request):
        data = request.data
        user = request.user.id
        userntfriend = UserNTFriend.objects.filter(user=user).first()
        data['user']= userntfriend.id
        post = Post.objects.get(id=data['id'])
        data['post'] = str(post.id)
        serializer = PostCommentSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'messages':serializer.errors,
                'status': False
            },status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        my_topic = f'mytopic_{post.user.id}'
        print(my_topic)
        data = serializer.data
        data['user'] = UserSerializer(userntfriend).data
        # print(UserSerializer(userntfriend).data)
        # print(data)
        asyncio.run(self.send_message_to_kafka(data, 'mytopic_commets'))

        notifileCommet = {
            "message": f'{userntfriend.name} đã bình luận về bài viết {post.caption} của bạn',
            "status":True
        }
        asyncio.run(self.send_message_to_kafka(notifileCommet, my_topic))

        return Response({
            "messages":"Comments succerfully",
            "status":True
        }, status=status.HTTP_200_OK)
        
