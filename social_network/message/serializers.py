from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import serializers

from .models import (PrivateMessage, PrivateMessageDetail, GroupMessage,
                     GroupMessageDetail, GroupMessageMember, GroupMessageMemberRole)
from user.models import User


class PrivateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        fields = '__all__'
        read_only_fields = ('created_time', 'updated_time')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        users = [instance.user_source, instance.user_target]
        users.remove(self.context.get("request").user)
        last_message = PrivateMessageDetail.objects.filter(message_id=instance.id).first()
        representation['user_id'] = users[0].id
        representation['user_name'] = users[0].first_name
        representation['avatar'] = "http://" + self.context['request'].get_host() + users[0].avatar.url if users[0].avatar else None
        representation['last_message'] = last_message.content if last_message is not None else ""
        del representation['user_source']
        del representation['user_target']
        return representation


class PrivateMessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessageDetail
        fields = '__all__'
        read_only_fields = ('created_time',)
        
    def create(self, validated_data):
        private_message = get_object_or_404(PrivateMessage, pk=validated_data['message_id'].id)
        message_detail = super().create(validated_data)
        private_message.updated_time = message_detail.created_time
        private_message.save()
        
        return message_detail
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_name'] = instance.user_id.first_name
        return representation
    
    
class GroupMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessage
        fields = '__all__'
        read_only_fields = ('created_time', 'updated_time')
        
    def save(self, **kwargs):
        is_created = self.instance is not None
        instance = super().save(**kwargs)
        if not is_created:
            admin_member = GroupMessageMember(group_message_id=instance, user_id=instance.created_by, invited_by=instance.created_by, role=GroupMessageMemberRole.OWNER)
            admin_member.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        last_message = GroupMessageDetail.objects.filter(group_message_id=instance.id).first()
        members = GroupMessageMember.objects.filter(
                                                    Q(group_message_id=instance.id)  &
                                                    ~Q(user_id= self.context['request'].user)
                                                ).values('user_id')
        members = [u['user_id'] for u in members]
        members = User.objects.filter(pk__in=members)
        members_avatar = [u.avatar for u in members]
        format_url = lambda avatar: "http://" + self.context['request'].get_host() + avatar.url if avatar else None
        members_avatar = [format_url(avatar) for avatar in members_avatar][:3]
        representation['last_message'] = last_message.content if last_message is not None else ""
        representation['group_avatar'] = members_avatar
        return representation


class GroupMessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessageDetail
        fields = '__all__'
        read_only_fields = ('created_time',)
        
    def create(self, validated_data):
        group_message = get_object_or_404(GroupMessage, pk=validated_data['group_message_id'].id)
        message_detail = super().create(validated_data)
        group_message.updated_time = message_detail.created_time
        group_message.save()
        
        return message_detail
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_name'] = instance.user_id.first_name
        return representation
     
        
class GroupMessageMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessageMember
        fields = '__all__'
        read_only_fields = ('created_time', 'updated_time')
      
    def to_representation(self, instance):
        user = instance.user_id
        representation = super().to_representation(instance)
        representation['avatar'] = "http://" + self.context['request'].get_host() + user.avatar.url if user.avatar else None
        return representation
        

class GroupMessageMemberRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessageMember
        fields = ['role', 'created_time', 'updated_time']
        read_only_fields = ('created_time', 'updated_time')

    def update(self, instance, validated_data):
        if instance.user_id == self.context.get("request").user:
            raise serializers.ValidationError({"user_id": "You can't do this action to yourself"})
        role_level = GroupMessageMemberRole.LEVELS
        cuser = self.context.get("view").get_current_member_object()
        print(role_level[validated_data['role']], role_level[cuser.role])
        if role_level[validated_data['role']] < role_level[cuser.role]:
            raise serializers.ValidationError({"role": "You cannot grant role higher than your current role"})
            
        return super().update(instance, validated_data)
    