from django.shortcuts import get_object_or_404
from rest_framework import permissions

from .models import GroupMessageMemberRole
    
class PrivateMessageDetailPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        private_message = view.get_private_message_object()
        if request.user in (private_message.user_source, private_message.user_target):
            return True
        return False
    

class GroupMessageMemberPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        group_message_members = view.get_group_member_objects()
        if group_message_members.filter(user_id=request.user).exists():
            return True
        return False
    
    
class GroupMessageMemberUpdateRemovePermission(GroupMessageMemberPermission):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            member = view.get_object()
            cuser = view.get_current_member_object()
            role_level = GroupMessageMemberRole.LEVELS
            print(role_level[member.role], role_level[cuser.role], role_level[GroupMessageMemberRole.MANAGER])
            if role_level[member.role] >= role_level[cuser.role] and role_level[cuser.role] <= role_level[GroupMessageMemberRole.MANAGER]:
                return True
        return False