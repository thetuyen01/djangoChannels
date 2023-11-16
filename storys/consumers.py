import asyncio
from aiokafka import AIOKafkaConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
from datetime import datetime
import json
from channels.db import database_sync_to_async
from .models import *
import time

class KafkaConsumerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.user_id_1 = self.scope['url_route']['kwargs']['id']
        await self.create_kafka_topic('my_topic_story', num_partitions=3, replication_factor=2)
        time.sleep(1)
        await self.setup_kafka_consumer('my_topic_story', self.user_id_1)
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
            try:
                data_dict = json.loads(data)
                list_user = data_dict.get("list_user", [])
                for user_id in list_user:
                    if user_id == int(self.user_id_1):
                        await self.send(text_data=data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {e}")

    async def create_kafka_topic(self, topic_name, num_partitions, replication_factor, broker_list='localhost:9092'):
        admin_client = AdminClient({'bootstrap.servers': broker_list})
        new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
        admin_client.create_topics([new_topic])