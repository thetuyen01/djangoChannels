from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from aiokafka import AIOKafkaProducer
import asyncio
from .models import *
from accounts.models import UserNTFriend
from .serializers import ChatGroupSerializer, ChatMessageSerializer
import json
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class ChatMessageAPIView(APIView):
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

    def post(self, request, user):
        if request.data:
            data = request.data.copy()  # Copy data to avoid modifying the original
            # data['sender'] = request.user.id
            my_user =UserNTFriend.objects.filter(user=request.user).first()
            data['sender'] = my_user.id
            serializer = ChatMessageSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    "message": serializer.errors,
                    "status": False
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()  # Save the serializer to create the ChatMessage instance
            if int(user) > int(my_user.id):
                my_topic = f'mytopic_{user}{my_user.id}'
            else:
                my_topic = f'mytopic_{my_user.id}{user}'
            print(user, my_user.id)
            print(my_topic)
            asyncio.run(self.send_message_to_kafka(serializer.data, my_topic))

            # Kiểm tra chatgroup có tồn tại không
            if not ChatGroup.objects.filter(chat_name=my_topic).exists():
                # tao nhom chat moi
                chatgroup = ChatGroup.objects.create(chat_name=my_topic)
                chatgroup.participants.add(user, my_user.id)
                chatgroup.messages.add(serializer.instance)

            # Lấy ra group
            chatgroup = ChatGroup.objects.get(chat_name=my_topic)
            # kiem tra xem user co ton tai trong group
            if not chatgroup.participants.filter(pk=my_user.id).exists():
                
                return Response({'message': 'user not Group does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
            chatgroup.messages.add(serializer.instance)  # Use the saved instance
            # gui tin nhan
            other_user = UserNTFriend.objects.get(id=user)
            ChatNotification.objects.create(chat = serializer.instance, user =other_user)
            return Response({'message': 'Message sent successfully', 'status':True}, status=status.HTTP_201_CREATED)
        
        return Response({'message':'not value post '}, status=status.HTTP_400_BAD_REQUEST)


class ChatGroupAPIView(APIView):
    def get(self, request): 
        try:
            my_user =UserNTFriend.objects.filter(user=request.user).first()
            chatgroup = ChatGroup.objects.filter(participants = my_user)
            serializer = ChatGroupSerializer(chatgroup, many=True)
            return Response({
                "data": serializer.data,
                "status":True
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': my_user})

