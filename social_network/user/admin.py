from django.contrib import admin
from .models import User, Friend, UserFollower

admin.site.register(User)
admin.site.register(Friend)
admin.site.register(UserFollower)