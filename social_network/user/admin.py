from django.contrib import admin
from .models import User, Friend, UserFollower


class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'first_name', 'last_name', 'last_login')


admin.site.register(User, UserAdmin)
admin.site.register(Friend)
admin.site.register(UserFollower)