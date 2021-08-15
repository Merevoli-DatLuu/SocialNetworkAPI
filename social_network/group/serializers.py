from rest_framework import serializers

from .models import Group, GroupFollower, GroupMember, GroupStatus, GroupMemberRole, GroupMemberStatus


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ('created_time', 'updated_time')
        
    def validate_status(value):
        if value == GroupStatus.BLOCKED:
            raise serializers.ValidationError("You can not set group status to blocked")
        return value
    
    def validate(self, attrs):
        attrs['updated_by'] = self.context.get('request').user
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data['owner'] = self.context.get("request").user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if "owner" in validated_data and instance.owner != validated_data['owner']:
            raise serializers.ValidationError("You can not change group's owner")
        return super().update(instance, validated_data)
    
    def save(self, **kwargs):
        is_created = self.instance is not None
        instance = super().save(**kwargs)
        if not is_created:
            admin_member = GroupMember(group_id=instance, user_id=instance.owner, role=GroupMemberRole.ADMIN)
            admin_member.save()
        return instance


class GroupFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupFollower
        fields = '__all__'
        read_only_fields = ('created_time', 'updated_time')
    

class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = '__all__'
        read_only_fields = ('created_time', 'updated_time')
        
        
class GroupMemberBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ['status', 'created_time', 'updated_time']
        read_only_fields = ('created_time', 'updated_time')
    
    def update(self, instance, validated_data):
        if instance.user_id == self.context.get("request").user:
            raise serializers.ValidationError({"user_id": "You can't do this action to yourself"})
        return super().update(instance, validated_data)
    
class GroupMemberRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ['role', 'created_time', 'updated_time']
        read_only_fields = ('created_time', 'updated_time')

    def update(self, instance, validated_data):
        if instance.user_id == self.context.get("request").user:
            raise serializers.ValidationError({"user_id": "You can't do this action to yourself"})
        return super().update(instance, validated_data)
            
            