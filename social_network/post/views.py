from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import viewsets

from .serializers import CommentSerilizer, CommentUpdateSerilizer, LikePostSerilizer, PostSerializer, PostUpdateSerializer, PostDetailSerializer
from user.serializers import UserSerializer
from .models import LikePost, Post, Comment, PUBLIC_STATUS, PRIVATE_STATUS
from .permissions import CommentCurrentUserPermission, PostCurrentUserPermission


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    
    def get_queryset(self):
        return Post.objects.filter(Q(mode=PUBLIC_STATUS) | (Q(mode=PRIVATE_STATUS) & Q(user_id = self.request.user)))
    
    def get_permissions(self):
        if self.action in ('update', 'destroy'):
            if len(self.permission_classes) == 1:
                self.permission_classes.append(PostCurrentUserPermission)
        elif len(self.permission_classes) == 2:
            self.permission_classes = [self.permission_classes[0]]            
        return super().get_permissions()
    
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'update':
            serializer_class = PostUpdateSerializer
        elif self.action == 'retrieve':
            serializer_class = PostDetailSerializer
        return serializer_class
    

class LikePostViewSet(viewsets.ModelViewSet):
    serializer_class = LikePostSerilizer
    
    def get_queryset(self):
        return LikePost.objects.filter(post_id=self.kwargs.get('post_id'))
    
    def get_object(self):
        post_id = self.kwargs.get('post_id', None)
        user_id = self.request.user.id
        try:
            return LikePost.objects.get(post_id=post_id, user_id=user_id)
        except LikePost.DoesNotExist:
            raise Http404
        
    def get_post(self):
        post_id = self.kwargs.get('post_id', None)
        return get_object_or_404(Post, pk = post_id)
    
    def perform_create(self, serializer):
        serializer.save(
            post_id = self.get_post(),
            user_id = self.request.user
        )
        
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'list':
            serializer_class = UserSerializer
        return serializer_class
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if self.action == "list":
            queryset = [likepost.user_id for likepost in queryset]
        
        return queryset
        

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerilizer
    
    def get_queryset(self):
        return Comment.objects.all()
    
    def get_permissions(self):
        if self.action in ('update', 'destroy'):
            if len(self.permission_classes) == 1:
                self.permission_classes.append(CommentCurrentUserPermission)
        elif len(self.permission_classes) == 2:
            self.permission_classes = [self.permission_classes[0]]            
        return super().get_permissions()
    
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'update':
            serializer_class = CommentUpdateSerilizer
        return serializer_class
        
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        
        if self.action == "list_comments":
            pk = self.kwargs['pk']
            if Post.objects.filter(pk=pk).exists():
                queryset = queryset.filter(post_id=pk, parent_comment=None)
            else:
                raise Http404
                
        elif self.action == "list_sub_comments":
            post_id = self.kwargs['post_id']
            comment_id = self.kwargs['comment_id']
            if queryset.filter(post_id=post_id, pk=comment_id):
                queryset = queryset.filter(post_id=post_id, parent_comment=comment_id)
            else:
                raise Http404
            
        return queryset
    
    def list_comments(self, request, pk=None):
        return super().list(request, pk)
            
    def list_sub_comments(self, request, post_id=None, comment_id=None):
        return super().list(request, post_id, comment_id)


post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'  
})

post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

likepost_detail = LikePostViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy'
})

comment_list = CommentViewSet.as_view({
    'get': 'list_comments',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy'  
})

comment_list_sub = CommentViewSet.as_view({
    'get': 'list_sub_comments'  
})


