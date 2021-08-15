from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import PrivateMessage, PrivateMessageDetail, GroupMessage, GroupMessageDetail, GroupMessageMember, GroupMessageMemberRole


class PrivateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        fields = '__all__'
        read_only_fields = ('created_time', 'updated_time')


class PrivateMessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessageDetail
        fields = '__all__'
        read_only_fields = ('created_time',)
        
    def create(self, validated_data):
        private_message = get_object_or_404(PrivateMessage, pk=validated_data['message_id'].id)
        message_detail = super().create(validated_data)
        private_message.updated_time = message_detail.created_time
        
        return message_detail
    
    
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


class GroupMessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessageDetail
        fields = '__all__'
        read_only_fields = ('created_time',)
        
    def create(self, validated_data):
        private_message = get_object_or_404(GroupMessage, pk=validated_data['group_message_id'].id)
        message_detail = super().create(validated_data)
        private_message.updated_time = message_detail.created_time
        
        return message_detail
     
        
class GroupMessageMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessageMember
        fields = '__all__'
        read_only_fields = ('created_time', 'updated_time')
        

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
    