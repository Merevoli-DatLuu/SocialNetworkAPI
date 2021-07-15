from rest_framework import permissions

class UserVerifyPermission(permissions.BasePermission):
    """
    Permission check for verified users
    """

    def has_permission(self, request, view):
        return request.user.is_verified