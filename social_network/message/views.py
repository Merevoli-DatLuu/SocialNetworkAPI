from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.db.models.query_utils import Q
from rest_framework import viewsets

from .models import PrivateMessage, PrivateMessageDetail, GroupMessage, GroupMessageDetail, GroupMessageMember
from .permissions import PrivateMessageDetailPermission, GroupMessageMemberPermission, GroupMessageMemberUpdateRemovePermission
from .serializers import GroupMessageMemberRoleSerializer, PrivateMessageSerializer, PrivateMessageDetailSerializer, GroupMessageSerializer, GroupMessageDetailSerializer, GroupMessageMemberSerializer


class PrivateMessageViewSet(viewsets.ModelViewSet):
    serializer_class = PrivateMessageSerializer
    
    def get_queryset(self):
        return PrivateMessage.objects.filter(Q(user_source=self.request.user) | (Q(user_target=self.request.user)))
    
    def create(self, request, *args, **kwargs):
        request.data['user_source'] = request.user.id
        request.data['user_target'] = self.kwargs['user_id']
        return super().create(request, *args, **kwargs)
    
    
class PrivateMessageDetailViewSet(viewsets.ModelViewSet):
    serializer_class = PrivateMessageDetailSerializer
    
    def get_queryset(self):
        return PrivateMessageDetail.objects.filter(message_id=self.kwargs['message_id'])
    
    def get_permissions(self):
        self.permission_classes = [self.permission_classes[0],  PrivateMessageDetailPermission]      
        return super().get_permissions()

    def get_private_message_object(self):
        return get_object_or_404(PrivateMessage, pk=self.kwargs['message_id'])

    def send_message(self, request, *args, **kwargs):
        request.data['message_id'] = self.kwargs['message_id']
        request.data['user_id'] = request.user.id
        return super().create(request, *args, **kwargs)
    
    
class GroupMessageViewSet(viewsets.ModelViewSet):
    serializer_class = GroupMessageSerializer
    
    def get_queryset(self):
        return GroupMessage.objects.filter(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        return super().create(request, *args, **kwargs)


class GroupMessageDetailViewSet(viewsets.ModelViewSet):
    serializer_class = GroupMessageDetailSerializer
    
    def get_queryset(self):
        return GroupMessageDetail.objects.filter(group_message_id=self.kwargs['group_message_id'])
    
    def get_permissions(self):
        self.permission_classes = [self.permission_classes[0],  GroupMessageMemberPermission]      
        return super().get_permissions()
    
    def get_group_member_objects(self):
        group_message_members = GroupMessageMember.objects.filter(group_message_id=self.kwargs['group_message_id'])
        if group_message_members.exists():
            return group_message_members
        else:
            raise Http404
    
    def send_message(self, request, *args, **kwargs):
        request.data['user_id'] = request.user.id
        request.data['group_message_id'] = self.kwargs['group_message_id']
        return super().create(request, *args, **kwargs)

    
class GroupMessageMemberViewSet(viewsets.ModelViewSet):
    serializer_class = GroupMessageMemberSerializer
    
    def get_queryset(self):
        return GroupMessageMember.objects.filter(group_message_id=self.kwargs['group_message_id'])
    
    def get_object(self):
        user_id = self.kwargs['user_id']
        return get_object_or_404(self.get_queryset(), user_id = user_id)
    
    def get_permissions(self):
        self.permission_classes = [self.permission_classes[0],  GroupMessageMemberPermission] 
        if self.action in ('update', 'destroy'):
            self.permission_classes.append(GroupMessageMemberUpdateRemovePermission)
        return super().get_permissions()
    
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'update':
            serializer_class = GroupMessageMemberRoleSerializer
        return serializer_class
    
    def get_current_member_object(self):
        return get_object_or_404(self.get_queryset(), user_id = self.request.user)
    
    def get_group_member_objects(self):
        group_message_members = GroupMessageMember.objects.filter(group_message_id=self.kwargs['group_message_id'])
        if group_message_members.exists():
            return group_message_members
        else:
            raise Http404
    
    def create(self, request, *args, **kwargs):
        request.data['invited_by'] = request.user.id
        request.data['group_message_id'] = self.kwargs['group_message_id']
        return super().create(request, *args, **kwargs)
    
    
private_message_list = PrivateMessageViewSet.as_view({
    'get': 'list',
})

private_message_create = PrivateMessageViewSet.as_view({
    'post': 'create'
})

private_message_detail_list_send = PrivateMessageDetailViewSet.as_view({
    'get': 'list',
    'post': 'send_message'
})

group_message_list_create = GroupMessageViewSet.as_view({
    'get': 'list',
    'post': 'create'
}) 

group_message_detail_list_send = GroupMessageDetailViewSet.as_view({
    'get': 'list',
    'post': 'send_message'
})

group_message_member_list_create = GroupMessageMemberViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

group_message_member_update_delete = GroupMessageMemberViewSet.as_view({
    'put': 'update',
    'delete': 'destroy'
})
        