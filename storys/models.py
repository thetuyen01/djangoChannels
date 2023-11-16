from django.db import models
from accounts.models import UserNTFriend


class Story(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(UserNTFriend, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='story_images/', null=True, blank=True)
    video_url = models.FileField(upload_to='story_video/', null=True, blank=True)

    def __str__(self):
        return str(self.title)

