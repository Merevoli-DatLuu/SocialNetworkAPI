from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager
from .validators import validate_secure_email, validate_age

class User(AbstractBaseUser):
    email           = models.EmailField(max_length=100, unique=True)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50, null=True)
    age             = models.PositiveIntegerField(validators=[validate_age], null=True)
    password        = models.CharField(max_length=100, validators=[validate_secure_email])
    is_verified     = models.BooleanField(default=False)

    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)


    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['first_name', 'age', 'password'] 

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True