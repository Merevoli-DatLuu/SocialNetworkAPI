from django.http import JsonResponse, Http404

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
    model = Post
    pagination_class = PageNumberPagination
    
    def get_permissions(self):
        permission_classes = [UserVerifyPermission]
        if self.action in ('update', 'destroy'):
            permission_classes += [PostCurrentUserPermission]
            
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = PostUpdateSerializer
            
        return serializer_class
    
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
        
    def list(self, request):
        posts = Post.objects.all()
        page = self.paginate_queryset(posts)
        serializer = self.get_serializer_class()(page, many=True)
        response = self.get_paginated_response(serializer.data)
        response.data = {
            'status': 'success',
            'message': 'list all posts succesfully',
            **response.data
        }
        return response

    def create(self, request):
        serializer = self.get_serializer_class()(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                'status': 'success',
                'message': 'add a new post succesfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        post = self.get_object(pk)
        serializer = self.get_serializer_class()(post)
        data = serializer.data
        data['total_of_likes'] = total_likes(pk)
        data['total_of_comment'] = total_comment(pk)
        data['is_liked'] = have_liked(pk, request.user.id)
        
        return Response({
            'status': 'success',
            'message': 'get a post succesfully',
            'data': data
        }, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        post = self.get_object(pk)
        serializer = self.get_serializer_class()(post, data = request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                'status': 'success',
                'message': 'update a new post succesfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)   
            
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
               
    def destroy(self, request, pk=None):
        post = self.get_object(pk)
        post.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': "Delete post successfully",
        }, status=status.HTTP_200_OK, safe=False)
    

class LikePostViewSet(viewsets.ModelViewSet):
    permission_classes = [UserVerifyPermission]
    serializer_class = LikePostSerilizer
    model = LikePost
    pagination_class = PageNumberPagination
    
    def get_object(self, post_id, user_id):
        try:
            return LikePost.objects.get(post_id=post_id, user_id=user_id)
        except LikePost.DoesNotExist:
            raise Http404
    
    def create(self, request, post_id=None):
        serializer = self.serializer_class(data = {
            'post_id': post_id,
            'user_id': request.user.id
        })
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                'status': 'success',
                'message': 'like succesfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, post_id=None):
        likepost = self.get_object(post_id, request.user.id)
        likepost.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': "unlike successfully",
        }, status=status.HTTP_200_OK, safe=False)
    
    def list(self, request, post_id):
        likeposts = self.model.objects.filter(post_id=post_id)
        users = [likepost.user_id for likepost in likeposts]
        page = self.paginate_queryset(users)
        serializer = UserSerializer(page, many=True)
        
        response = self.get_paginated_response(serializer.data)
        response.data = {
            'status': 'success',
            'message': 'list all user that liked post succesfully',
            **response.data
        }
        return response


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [UserVerifyPermission]
    serializer_class = CommentSerilizer
    model = Comment
    pagination_class = PageNumberPagination
    
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = CommentUpdateSerilizer
            
        return serializer_class
    
    def get_object(self, comment_id):
        try:
            return Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise Http404
        
    def list_comments(self, request, pk=None):
        comments = self.model.objects.filter(post_id=pk, parent_comment=None)
        page = self.paginate_queryset(comments)
        serializer = self.get_serializer_class()(page, many=True)
        response = self.get_paginated_response(serializer.data)
        response.data = {
            'status': 'success',
            'message': 'list all comment succesfully',
            **response.data
        }
        return response
            
    
    def list_sub_comments(self, request, post_id=None, comment_id=None):
        comments = self.model.objects.filter(post_id=post_id, parent_comment=comment_id)
        page = self.paginate_queryset(comments)
        serializer = self.get_serializer_class()(page, many=True)
        response = self.get_paginated_response(serializer.data)
        response.data = {
            'status': 'success',
            'message': 'list all comment succesfully',
            **response.data
        }
        return response
    
    def create(self, request, pk=None):
        serializer = self.get_serializer_class()(data = {
            'post_id': pk,
            'user_id': request.user.id,
            **request.data
        })
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                'status': 'success',
                'message': 'like succesfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        comment = self.get_object(pk)
        serializer = self.get_serializer_class()(comment, data = request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                'status': 'success',
                'message': 'update a new post succesfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED) 
              
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        comment = self.get_object(pk)
        comment.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': "delete comment successfully",
        }, status=status.HTTP_200_OK, safe=False)


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


