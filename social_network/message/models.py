from django.db import models

from user.models import User


class GroupMessageMemberRole(object):
    OWNER  = "Owner"
    MANAGER = "Manager"
    MEMBER  = "Member"
    CHOICES = [
        (OWNER, OWNER),
        (MANAGER, MANAGER),
        (MEMBER, MEMBER)
    ]
    LEVELS = {
        OWNER: 1,
        MANAGER: 2,
        MEMBER: 3
    }  

    
class PrivateMessage(models.Model):
    user_source             = models.ForeignKey(User, on_delete=models.CASCADE, related_name="private_message_user_source")
    user_target             = models.ForeignKey(User, on_delete=models.CASCADE, related_name="private_message_user_target")
    created_time            = models.DateTimeField(auto_now_add=True)
    updated_time            = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user_source', 'user_target')
        ordering = ('updated_time',)
    
    def __str__(self):
        return f"{self.id} | {self.user_source} | {self.user_target}" 

    
class PrivateMessageDetail(models.Model):
    message_id              = models.ForeignKey(PrivateMessage, on_delete=models.CASCADE)
    user_id                 = models.ForeignKey(User, on_delete=models.CASCADE)
    content                 = models.TextField()
    created_time            = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('created_time',)
    
    def __str__(self):
        return f"{self.id} | {self.message_id} | {self.user_id}" 
    

class GroupMessage(models.Model):
    name                    = models.CharField(max_length=128)
    created_by              = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time            = models.DateTimeField(auto_now_add=True)
    updated_time            = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('updated_time',)
    
    def __str__(self):
        return f"{self.id} | {self.name} | {self.created_by}" 
    
    
class GroupMessageDetail(models.Model):
    group_message_id        = models.ForeignKey(GroupMessage, on_delete=models.CASCADE)
    user_id                 = models.ForeignKey(User, on_delete=models.CASCADE)
    content                 = models.TextField()
    created_time            = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('created_time',)
    
    def __str__(self):
        return f"{self.id} | {self.group_message_id} | {self.user_id}" 


class GroupMessageMember(models.Model):
    group_message_id        = models.ForeignKey(GroupMessage, on_delete=models.CASCADE)
    user_id                 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_message_member_user_id")
    invited_by              = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_message_member_invited_by")
    role                    = models.CharField(
                                max_length=10,
                                choices=GroupMessageMemberRole.CHOICES,
                                default=GroupMessageMemberRole.MEMBER,
                            )
    created_time            = models.DateTimeField(auto_now_add=True)
    updated_time            = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('group_message_id', 'user_id')
        
    def __str__(self):
        return f"{self.id} | {self.group_message_id} | {self.user_id}" 
    