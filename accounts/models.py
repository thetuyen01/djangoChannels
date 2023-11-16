from django.db import models
from django.contrib.auth.models import User

class UserNTFriend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="user")
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/',null=False, blank=False)

    def __str__(self) -> str:
        return str(self.name)

