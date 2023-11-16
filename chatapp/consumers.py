import asyncio
from aiokafka import AIOKafkaConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
from datetime import datetime
import json
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import *
from accounts.models import UserNTFriend
import time
class KafkaConsumerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        user_id_1 = self.scope['url_route']['kwargs']['custom_string'].split('-')[0]
        user_id_2 = self.scope['url_route']['kwargs']['custom_string'].split('-')[1]
        print(self.scope['url_route']['kwargs']['custom_string'])
        print(user_id_1, user_id_2)
        if int(user_id_1) > int(user_id_2):
            my_topic = f'mytopic_{user_id_1}{user_id_2}'
        else:
            my_topic = f'mytopic_{user_id_2}{user_id_1}'

        print(my_topic)
        await self.create_kafka_topic(my_topic, num_partitions=3, replication_factor=2)
        time.sleep(1)
        await self.setup_kafka_consumer(my_topic, user_id_1)
    async def setup_kafka_consumer(self, my_topic, user_id_1):
        self.kafka_consumer = AIOKafkaConsumer(
            my_topic,
            bootstrap_servers='localhost:9092',
            group_id=f"{user_id_1}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            auto_offset_reset='latest'
        )
        await self.kafka_consumer.start()
        asyncio.ensure_future(self.process_messages())

    async def disconnect(self, close_code):
        await self.kafka_consumer.stop()

    async def process_messages(self):
        async for msg in self.kafka_consumer:
            data = msg.value.decode('utf-8')
            await self.send(text_data=data)

    async def create_kafka_topic(self, topic_name, num_partitions, replication_factor, broker_list='localhost:9092'):
        admin_client = AdminClient({'bootstrap.servers': broker_list})
        new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
        admin_client.create_topics([new_topic])


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "user"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        user_id = data['user_id']
        connection_type = data['type']
        if connection_type == 'close':
            await self.change_online_status(user_id, 'close')
        else:
            await self.change_online_status(user_id, connection_type)
            

    async def send_onlineStatus(self, event):
        data = json.loads(event.get('value'))
        self.user_id = data['user_id']
        online_status = data['status']
        
        await self.send(text_data=json.dumps({
            'user_id': self.user_id,
            'online_status': online_status
        }))

    async def disconnect(self, message):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.change_online_status(self.user_id, 'close')

    @database_sync_to_async
    def change_online_status(self, user_id, c_type):
        userntfriend = UserNTFriend.objects.get(id = int(user_id))
        print(userntfriend)
        userprofile = UserProfileModel.objects.filter(user=userntfriend.id).first()
        print(userprofile)
        if c_type == 'open':
            userprofile.online_status = True
            userprofile.save()
        else:
            userprofile.online_status = False
            userprofile.save()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'{user_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        data = json.loads(event.get('value'))
        count = data['count']
        message = data['message']
        await self.send(text_data=json.dumps({
            "count":count,
            "message":message
        }))