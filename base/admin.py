from django.contrib import admin

from .models import Room, Topic, Message, User, BlogPost

admin.site.register(User)
admin.site.register(BlogPost)
admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Message)
