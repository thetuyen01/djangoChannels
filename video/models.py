from django.db import models
from accounts.models import UserNTFriend


class Video(models.Model):
    user = models.ForeignKey(UserNTFriend, on_delete=models.CASCADE)
    description = models.TextField()
    video_url = models.FileField(upload_to='video/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name
    
class CommentVideo(models.Model):
    user = models.ForeignKey(UserNTFriend, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Like(models.Model):
    user = models.ForeignKey(UserNTFriend, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name