from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager
from .validators import validate_secure_email, validate_age


class FriendStatus(object):
    NEW = "New"
    ACCEPT = "Accept"
    CHOICES = [
        (NEW, NEW),
        (ACCEPT, ACCEPT)
    ]


def user_avatar_directory_path(instance, filename):
    hex_dump = 0
    base = 1
    for c in instance.email:
        hex_dump += ord(c)*base
        base *= 256
    hex_dump = hex(hex_dump)[2:10] 
    file_extension = filename.split('.')[-1]
    return 'avatar/avatar-{:04d}-{}.{}'.format(instance.id, hex_dump, file_extension)
    
    
class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    age = models.PositiveIntegerField(validators=[validate_age], null=True)
    password = models.CharField(max_length=100,
                                validators=[validate_secure_email])
    is_verified = models.BooleanField(default=False)
    avatar      = models.ImageField(upload_to=user_avatar_directory_path, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'age', 'password']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    


class Friend(models.Model):
    user_source             = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="friend_user_source")
    user_target             = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="friend_user_target")
    status                  = models.CharField(
                                max_length=10,
                                choices=FriendStatus.CHOICES,
                                default=FriendStatus.NEW,
                            )
    created_time            = models.DateTimeField(auto_now_add=True)
    updated_time            = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user_source', 'user_target')
    
    def __str__(self):
        return f"{self.id} | {self.user_source} | {self.user_target}" 

    
class UserFollower(models.Model):
    user_source             = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follower_source")
    user_target             = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follower_target")
    created_time            = models.DateTimeField(auto_now_add=True)
    updated_time            = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user_source', 'user_target')
    
    def __str__(self):
        return f"{self.id} | {self.user_source} | {self.user_target}" 