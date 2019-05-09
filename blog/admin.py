from django.contrib import admin

# Register your models here.
from .models import Post, Request, FriendshipRequest

admin.site.register(Post)
admin.site.register(Request)
admin.site.register(FriendshipRequest)
