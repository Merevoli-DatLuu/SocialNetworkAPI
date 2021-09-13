from django.db.models.query_utils import Q
from django.http import request
from django.shortcuts import get_object_or_404
from django.urls.base import set_urlconf
from rest_framework import viewsets

from user.models import User
from user.serializers import UserSerializer
from .models import Group, GroupMember, GroupFollower, GroupMemberRole, GroupMemberStatus
from .serializers import (GroupSerializer, GroupFollowerSerializer, GroupMemberSerializer
                          , GroupMemberBlockSerializer, GroupMemberRoleSerializer)
from .permissions import (GroupActivePermission, GroupMemberAdminPermission,
                          GroupNotBlockedPermission, GroupPublicFollowerPermission,
                          GroupInvitationAcceptDenyPermission)

class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    
    def get_queryset(self):
        return Group.objects.all()
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
    
        if self.action == 'list_owner':
            queryset = queryset.filter(owner = self.request.user)
        if self.action == 'list_joined':
            queryset = GroupMember.objects.filter(user_id = self.request.user).values('group_id')
            groups = set([p['group_id'] for p in queryset])
            queryset = Group.objects.filter(pk__in=groups)
            
        return queryset
    
    def list_onwer(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def list_joined(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class GroupFollowerViewSet(viewsets.ModelViewSet):
    serializer_class = GroupFollowerSerializer
    
    def get_permissions(self):
        self.permission_classes = [self.permission_classes[0], GroupActivePermission, GroupPublicFollowerPermission]            
        if self.action == "list_following":
            self.permission_classes = [self.permission_classes[0]]
        return super().get_permissions()
    
    def get_queryset(self):
        return GroupFollower.objects.all()
    
    def filter_queryset(self, queryset):
        if self.action == "list_follower":
            queryset = self.get_queryset().filter(group_id=self.kwargs['pk']).values('user_id')
            users = [u['user_id'] for u in queryset]
            queryset = User.objects.filter(pk__in=users)
        elif self.action == "list_following":
            queryset = self.get_queryset().filter(user_id=self.request.user).values('group_id')
            groups = [p['group_id'] for p in queryset]
            queryset = Group.objects.filter(pk__in=groups)
            
        return queryset
    
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'list_follower':
            serializer_class = UserSerializer
        elif self.action == 'list_following':
            serializer_class = GroupSerializer
        return serializer_class
    
    def get_object(self):
        group_id = self.kwargs.get('pk', None)
        user_id = self.request.user.id
        return get_object_or_404(self.get_queryset(), group_id=group_id, user_id=user_id)
    
    def get_group_object(self):
        group_id = self.kwargs.get('pk', None)
        return get_object_or_404(Group, pk=group_id)
    
    def create(self, request, *args, **kwargs):
        request.data['group_id'] = self.kwargs['pk']
        request.data['user_id'] = request.user.id
        return super().create(request, *args, **kwargs)
    
    def list_follower(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
    
    def list_following(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class GroupMemberViewSet(viewsets.ModelViewSet):
    serializer_class = GroupMemberSerializer
    
    def get_queryset(self):
        group_id = self.kwargs.get('pk', None)
        return GroupMember.objects.filter(group_id = group_id)
    
    def filter_queryset(self, queryset):
        if self.action == 'list_active':
            queryset = queryset.filter(status = GroupMemberStatus.ACTIVE)
        elif self.action == 'list_blocked':
            queryset = queryset.filter(status = GroupMemberStatus.BLOCKED)
        return queryset
    
    def get_object(self):
        group_id = self.kwargs.get('pk', None)
        user_id = self.kwargs.get('user_id', None)
        return get_object_or_404(self.get_queryset(), group_id=group_id, user_id=user_id)
    
    def get_group_object(self):
        group_id = self.kwargs.get('pk', None)
        return get_object_or_404(Group, pk=group_id)
    
    def get_permissions(self):
        self.permission_classes = [self.permission_classes[0], GroupMemberAdminPermission]            
        return super().get_permissions()
    
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action in ('update_block', 'update_unblock'):
            serializer_class = GroupMemberBlockSerializer
        if self.action == 'update_role':
            serializer_class = GroupMemberRoleSerializer
        return serializer_class
    
    def create(self, request, *args, **kwargs):
        request.data['group_id'] = self.kwargs['pk']
        return super().create(request, *args, **kwargs)
    
    def list_active(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def list_blocked(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def update_block(self, request, *args, **kwargs):
        request.data['status'] = GroupMemberStatus.BLOCKED
        return super().partial_update(request, *args, **kwargs)
    
    def update_unblock(self, request, *args, **kwargs):
        request.data['status'] = GroupMemberStatus.ACTIVE
        return super().partial_update(request, *args, **kwargs)
    
    def update_role(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    

class GroupInvitationViewSet(viewsets.ModelViewSet):
    serializer_class = GroupMemberSerializer
    
    def get_permissions(self):
        self.permission_classes = [self.permission_classes[0],  GroupPublicFollowerPermission]            
        if self.action in ('list_invitation', 'accept_invatition', 'deny_invatition'):
            self.permission_classes.append(GroupInvitationAcceptDenyPermission)
        return super().get_permissions()
    
    def get_object(self):
        group_id = self.kwargs.get('pk', None)
        if 'user_id' in self.kwargs:
            user_id = self.kwargs.get('user_id', None)
        else:
            user_id = self.request.user.id
        return get_object_or_404(self.get_queryset(), group_id=group_id, user_id=user_id)
    
    def get_group_object(self):
        group_id = self.kwargs.get('pk', None)
        return get_object_or_404(Group, pk=group_id)
    
    def get_queryset(self):
        return GroupMember.objects.filter(status = GroupMemberStatus.PENDING)
    
    def filter_queryset(self, queryset):
        if self.action == 'list_invitation':
            group_id = self.kwargs.get('pk', None)
            queryset = queryset.filter(group_id = group_id)
        if self.action == 'list_inviting':
            queryset = self.get_queryset().filter(user_id = self.request.user).values('group_id')
            groups = [p['group_id'] for p in queryset]
            queryset = Group.objects.filter(pk__in=groups)
            
        return queryset
    
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'list_inviting':
            serializer_class = GroupSerializer
        elif self.action == 'update':
            serializer_class = GroupMemberBlockSerializer
        
        return serializer_class
    
    def list_invitation(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def list_inviting(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def accept_invatition(self, request, *args, **kwargs):
        request.data['status'] = GroupMemberStatus.ACTIVE
        return super().partial_update(request, *args, **kwargs)
    
    def deny_invatition(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def send_invitaton(self, request, *args, **kwargs):
        request.data['group_id'] = self.kwargs['pk']
        request.data['user_id'] = request.user.id
        request.data['role'] = GroupMemberRole.MEMBER
        request.data['status'] = GroupMemberStatus.PENDING
        return super().create(request, *args, **kwargs)
    
    def cancel_invitaton(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    
group_list = GroupViewSet.as_view({
    'get': 'list_onwer',
    'post': 'create'
})

group_list_joined = GroupViewSet.as_view({
    'get': 'list_joined'
})

group_detail = GroupViewSet.as_view({
    'get': 'retrieve',
    'put': 'partial_update',
    'delete': 'destroy'
})

group_follower_change = GroupFollowerViewSet.as_view({
    'post': 'create',
    'delete': 'destroy'  
})

group_follower_list_follower = GroupFollowerViewSet.as_view({
    'get': 'list_follower'  
})


group_follower_list_following = GroupFollowerViewSet.as_view({
    'get': 'list_following'  
})

group_member_list = GroupMemberViewSet.as_view({
    'post': 'create',
    'get': 'list_active'
})

group_member_list_blocked = GroupMemberViewSet.as_view({
    'get': 'list_blocked'
})

group_member_delete = GroupMemberViewSet.as_view({
    'delete': 'destroy',
})

group_member_block = GroupMemberViewSet.as_view({
    'put': 'update_block',
})

group_member_unblock = GroupMemberViewSet.as_view({
    'put': 'update_unblock',
})

group_member_role = GroupMemberViewSet.as_view({
    'put': 'update_role'  
})

group_invitation_list_send = GroupInvitationViewSet.as_view({
    'get': 'list_invitation',
    'post': 'send_invitaton'
})

group_invitation_list_inviting = GroupInvitationViewSet.as_view({
    'get': 'list_inviting'
})

group_invitation_accept = GroupInvitationViewSet.as_view({
    'put': 'accept_invatition'
})

group_invitation_deny = GroupInvitationViewSet.as_view({
    'delete': 'deny_invatition'
})

group_invitation_cancel = GroupInvitationViewSet.as_view({
    'delete': 'cancel_invitaton'
})