from django.contrib import admin

from .models import PrivateMessage, PrivateMessageDetail, GroupMessage, GroupMessageDetail, GroupMessageMember
    
    
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'updated_time')
    
class PrivateMessageDetailAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'content', 'created_time')
    
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'updated_time')
    
class GroupMessageDetailAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'content', 'created_time')
    
    
admin.site.register(PrivateMessage, PrivateMessageAdmin)
admin.site.register(PrivateMessageDetail, PrivateMessageDetailAdmin)
admin.site.register(GroupMessage, GroupMessageAdmin)
admin.site.register(GroupMessageDetail, GroupMessageDetailAdmin)
admin.site.register(GroupMessageMember)