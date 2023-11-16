from django.db import models
from accounts.models import UserNTFriend

class ChatMessage(models.Model):
    sender = models.ForeignKey(UserNTFriend, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='static/image_chatapp', blank=True, null=True)
    file = models.FileField(upload_to='static/file_chatapp', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.name} - {self.content}"
    


class ChatGroup(models.Model):
    chat_name = models.CharField(max_length=100)
    participants = models.ManyToManyField(UserNTFriend, related_name='chat_groups')
    messages = models.ManyToManyField(ChatMessage, related_name='chat_groups', blank=True, null=True)

    def __str__(self):
        participant_list = ", ".join([str(user) for user in self.participants.all()])
        return f"Chat Group ({participant_list})"




class UserProfileModel(models.Model):
    user = models.OneToOneField(UserNTFriend, on_delete=models.CASCADE)
    online_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.user.name)
    

class ChatNotification(models.Model):
    chat = models.ForeignKey(ChatMessage, on_delete=models.CASCADE)
    user = models.ForeignKey(UserNTFriend, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.user.name)