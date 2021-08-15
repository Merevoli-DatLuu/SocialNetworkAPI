from django.contrib import admin
from .models import Group, GroupFollower, GroupMember


class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'role')
    
    
admin.site.register(Group)
admin.site.register(GroupFollower)
admin.site.register(GroupMember, GroupMemberAdmin)