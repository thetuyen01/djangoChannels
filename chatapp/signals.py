from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from accounts.models import UserNTFriend
import json

@receiver(post_save, sender = UserProfileModel)
def send_onlineStatus(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        user = instance.user
        user_status = instance.online_status

        data = {
            'user_id': user.id,
            'status': user_status
        }

        async_to_sync(channel_layer.group_send)(
            'user',{
                'type':'send_onlineStatus',
                'value': json.dumps(data)
            }
            
        )

@receiver(post_save, sender = ChatNotification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        notification_obj = ChatNotification.objects.filter(is_seen=False, user = instance.user).count()
        user_id = str(instance.user.id)
        data = {
            'count':notification_obj,
            "message": f'{instance.chat.sender.name} đã gửi tin nhắn cho bạn'
        }

        async_to_sync(channel_layer.group_send)(
            user_id,{
                'type':'send_notification',
                'value':json.dumps(data)
            }
        )