from django.contrib import admin

from .models import PrivateMessage, PrivateMessageDetail, GroupMessage, GroupMessageDetail, GroupMessageMember
    
    
class PrivateMessageDetailAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'content')
    
    
class GroupMessageDetailAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'content')
    
    
admin.site.register(PrivateMessage)
admin.site.register(PrivateMessageDetail, PrivateMessageDetailAdmin)
admin.site.register(GroupMessage)
admin.site.register(GroupMessageDetail, GroupMessageDetailAdmin)
admin.site.register(GroupMessageMember)