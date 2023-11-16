from django.contrib import admin

from .models import *

admin.site.register([Tag, Post, Follow, Stream, Comment, CommentNotification])
