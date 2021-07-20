from rest_framework import permissions
from allauth.account.models import EmailAddress 
    
class UserVerifyPermission(permissions.IsAuthenticated):
    """
    Permission check for verified users
    """

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            user = EmailAddress.objects.get(email=request.user.email)
            return user.verified
        return False
    
