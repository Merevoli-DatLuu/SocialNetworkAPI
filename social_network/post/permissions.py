from django.http import Http404
from rest_framework import permissions
from .models import Post, Comment
    
class PostCurrentUserPermission(permissions.BasePermission):
    """
    Permission check for correct user
    """

    def has_permission(self, request, view):
        post_id = request._request.path_info.split('/')[-1]
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise Http404
        user_id = post.user_id.id
        return user_id == request.user.id
    
class CommentCurrentUserPermission(permissions.BasePermission):
    """
    Permission check for correct user
    """

    def has_permission(self, request, view):
        comment_id = request._request.path_info.split('/')[-1]
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise Http404
        user_id = comment.user_id.id
        return user_id == request.user.id
    
