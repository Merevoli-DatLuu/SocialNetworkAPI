from django.db import models

from user.models import User


class GroupType(object):
    PUBLIC  = "Public"
    PRIVATE = "Private"
    SECRET  = "Secret"
    CHOICES = [
        (PUBLIC, PUBLIC),
        (PRIVATE, PRIVATE),
        (SECRET, SECRET)
    ]
    
    
class GroupStatus(object):
    ACTIVE  = "Active"
    CLOSED  = "Closed"
    BLOCKED = "Blocked"
    CHOICES = [
        (ACTIVE, ACTIVE),
        (CLOSED, CLOSED),
        (BLOCKED, BLOCKED)
    ]
    
    
class GroupMemberRole(object):
    ADMIN       = "Admin"
    MODERATOR   = "Moderator"
    MEMBER      = "Member"
    CHOICES     = [
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (MEMBER, MEMBER) 
    ]
    
    
class GroupMemberStatus(object):
    PENDING     = "Pending"
    ACTIVE      = "Active"
    BLOCKED     = "Blocked"
    CHOICES     = [
        (PENDING, PENDING),
        (ACTIVE, ACTIVE),
        (BLOCKED, BLOCKED), 
    ]
    
    
class Group(models.Model):
    name                    = models.CharField(max_length=200)
    description             = models.TextField()
    type                    = models.CharField(
                                max_length=10,
                                choices=GroupType.CHOICES,
                                default=GroupType.PUBLIC,
                            )
    status                  = models.CharField(
                                max_length=10,
                                choices=GroupStatus.CHOICES,
                                default=GroupStatus.ACTIVE,
                            )
    owner                   = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='group_owner')
    updated_by              = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='group_updated_by')
    created_time            = models.DateTimeField(auto_now_add=True)
    updated_time            = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return f"[ {self.id} | {self.name} | {self.owner} ]" 
    

class GroupMember(models.Model):
    group_id                = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id                 = models.ForeignKey(User, on_delete=models.CASCADE)
    role                    = models.CharField(
                                max_length=10,
                                choices=GroupMemberRole.CHOICES,
                                default=GroupMemberRole.MEMBER,
                            )
    status                  = models.CharField(
                                max_length=10,
                                choices=GroupMemberStatus.CHOICES,
                                default=GroupMemberStatus.ACTIVE,
                            )
    created_time            = models.DateTimeField(auto_now_add=True)
    updated_time            = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('group_id', 'user_id')
        ordering = ['id']
        
    def __str__(self):
        return f"[ {self.id} | {self.group_id} | {self.user_id} ]" 
    
    
class GroupFollower(models.Model):
    group_id                = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id                 = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time            = models.DateTimeField(auto_now_add=True)
    updated_time            = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('group_id', 'user_id')
        
    def __str__(self):
        return f"[ {self.id} | {self.group_id} | {self.user_id} ]" 
    