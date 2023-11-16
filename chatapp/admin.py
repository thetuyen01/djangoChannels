from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ChatGroup)
admin.site.register(ChatMessage)
admin.site.register(UserProfileModel)
admin.site.register(ChatNotification)
