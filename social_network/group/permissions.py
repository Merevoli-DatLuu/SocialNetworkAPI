from rest_framework import permissions

from .models import GroupMemberRole, GroupStatus, GroupType, GroupMember, GroupMemberStatus
    
class GroupNotBlockedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        group = view.get_object()
        if group.status == GroupStatus.BLOCKED:
            return False
        return True
    
    
class GroupActivePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        group = view.get_group_object()
        if group.status != GroupStatus.ACTIVE:
            return False
        return True
    
    
class GroupPublicFollowerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        group = view.get_group_object()
        
        if group.type == GroupType.PUBLIC:
            return True
        
        user = request.user
        user = GroupMember.objects.filter(group_id=group, user_id=user)
        if len(user) > 0:
            user = user[0]
            if user.status == GroupMemberStatus.ACTIVE:
                return True
        return False
    

class GroupMemberAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        group_id = view.get_group_object()
        user = GroupMember.objects.filter(group_id=group_id, user_id=user)
        
        if 'user_id' in view.kwargs:
            member = view.get_object()
            if member.status == GroupMemberStatus.PENDING:
                return False
        
        if len(user) > 0:
            user = user[0]
            if user.role == GroupMemberRole.ADMIN and user.status == GroupMemberStatus.ACTIVE:
                return True
        return False
    
    
class GroupInvitationAcceptDenyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        group_id = view.get_group_object()
        user = GroupMember.objects.filter(group_id=group_id, user_id=user)
        
        if 'user_id' in view.kwargs:
            member = view.get_object()
            if member.status != GroupMemberStatus.PENDING:
                return False
        
        if len(user) > 0:
            user = user[0]
            if user.role in (GroupMemberRole.ADMIN, GroupMemberRole.MODERATOR) and user.status == GroupMemberStatus.ACTIVE:
                return True
            
        return False