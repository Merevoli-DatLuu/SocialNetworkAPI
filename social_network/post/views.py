from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import CommentSerilizer, CommentUpdateSerilizer, LikePostSerilizer, PostSerializer, PostUpdateSerializer
from user.serializers import UserSerializer
from .models import LikePost, Post, Comment
from user.permissions import UserVerifyPermission
from .permissions import PostCurrentUserPermission
from .utils import total_comment, total_likes, have_liked


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    queryset = Post.objects.all()
    
    def get_permissions(self):
        self.permission_classes = [UserVerifyPermission]
        if self.action in ('update', 'destroy'):
            self.permission_classes += [PostCurrentUserPermission]
        return super().get_permissions()
    
    def get_serializer_class(self):
        self.serializer_class = self.serializer_class
        if self.action == 'update':
            self.serializer_class = PostUpdateSerializer
        return super().get_serializer_class()

    def retrieve(self, request, pk=None):
        response = super().retrieve(request, pk)
        response.data.update({
            'total_of_likes': total_likes(pk),
            'total_of_comment': total_comment(pk),
            'is_liked': have_liked(pk, request.user.id)
        })   
        return response
    

class LikePostViewSet(viewsets.ModelViewSet):
    permission_classes = [UserVerifyPermission]
    serializer_class = LikePostSerilizer
    model = LikePost
    pagination_class = PageNumberPagination
    queryset = Post.objects.all()
    
    def get_object(self):
        post_id = self.kwargs.get('post_id', None)
        user_id = self.request.user.id
        try:
            return LikePost.objects.get(post_id=post_id, user_id=user_id)
        except LikePost.DoesNotExist:
            raise Http404
    
    def create(self, request, post_id=None):
        serializer = self.get_serializer(data = {
            'post_id': post_id,
            'user_id': request.user.id
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request, post_id):
        likeposts = self.model.objects.filter(post_id=post_id)
        users = [likepost.user_id for likepost in likeposts]
        page = self.paginate_queryset(users)
        serializer = UserSerializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        
        return response
        

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [UserVerifyPermission]
    serializer_class = CommentSerilizer
    pagination_class = PageNumberPagination
    queryset = Comment.objects.all()
    
    def get_serializer_class(self):
        self.serializer_class = self.serializer_class
        if self.action == 'update':
            self.serializer_class = CommentUpdateSerilizer
        return super().get_serializer_class()
        
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        
        if self.action == "list_comments":
            pk = self.kwargs['pk']
            queryset = queryset.filter(post_id=pk, parent_comment=None)
        elif self.action == "list_sub_comments":
            post_id = self.kwargs['post_id']
            comment_id = self.kwargs['comment_id']
            queryset = queryset.filter(post_id=post_id, parent_comment=comment_id)
            
        return queryset
    
    def list_comments(self, request, pk=None):
        return super().list(request, pk)
            
    def list_sub_comments(self, request, post_id=None, comment_id=None):
        return super().list(request, post_id, comment_id)
    
    def create(self, request, pk=None):
        serializer = self.get_serializer_class()(data = {
            'post_id': pk,
            'user_id': request.user.id,
            **request.data
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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


