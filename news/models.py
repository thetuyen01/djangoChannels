from audioop import reverse
from django.db import models
from accounts.models import UserNTFriend
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
import uuid

class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tag")
    slug = models.SlugField(null=False, unique=True, default=uuid.uuid1)
    

    def __str__(self):
        return str(self.title)
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to='image_post/', verbose_name="Picture", null=True, blank=True)
    caption = models.CharField(max_length=100000, verbose_name="Caption", blank=True, null=True)
    posted = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, related_name="tags", blank=True, null=True)
    user = models.ForeignKey(UserNTFriend, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.caption)

    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name="Comment Text")
    user = models.ForeignKey(UserNTFriend, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    

class Follow(models.Model):
    follower = models.ForeignKey(UserNTFriend, on_delete=models.CASCADE, related_name="Follower")
    following = models.ForeignKey(UserNTFriend, on_delete=models.CASCADE, related_name="Following")


class Stream(models.Model):
    following = models.ForeignKey(UserNTFriend, on_delete=models.CASCADE, related_name="Stream_Following")
    user = models.ForeignKey(UserNTFriend, on_delete=models.CASCADE, related_name="Stream_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date = post.posted, following=user)
            stream.save()

post_save.connect(Stream.add_post, sender=Post)


class CommentNotification(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(UserNTFriend, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.user.name)


