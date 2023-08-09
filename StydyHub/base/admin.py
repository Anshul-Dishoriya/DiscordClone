from django.contrib import admin
from base.models import Room, Topic, Message , UserFollowing , UserFollowers

# Register your models here.

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(UserFollowers)
admin.site.register(UserFollowing)




