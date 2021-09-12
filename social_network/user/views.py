from django.http import Http404
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, PasswordChangeView
from rest_framework import viewsets

from .serializers import FriendSerializer, UserFollowerSerializer, UserRegisterSerializer, UserLoginSerializer, UserSerializer, UserChangePasswordSerializer
from .models import Friend, FriendStatus, User, UserFollower
from .exceptions import FriendAlreadyAcceptException, FriendAlreadyDenyException, FriendAlreadyException, FriendNotYourException
from .permissions import UserVerifyPermission


class UserRegisterView(RegisterView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


class UserLoginView(LoginView):
    serializer_class = UserLoginSerializer


class UserChangePasswordView(PasswordChangeView):
    permission_classes = (UserVerifyPermission,)
    serializer_class = UserChangePasswordSerializer
    
        
class UserProfileView(RetrieveAPIView):
    permission_classes = (UserVerifyPermission, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class UserDetailView(RetrieveAPIView):
    permission_classes = (UserVerifyPermission, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        pk = self.kwargs.get('user_id', None)
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        

class UserListView(ListAPIView):
    permission_classes = (UserVerifyPermission, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset.all().exclude(email = self.request.user.email)


class FriendViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    
    def get_queryset(self):
        return Friend.objects.all()
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        if self.action == "list_friend":
            suser = self.request.user.id
        elif self.action == "list_friend_others":
            suser = self.kwargs['user_id']
        
        if self.action in ("list_friend", "list_friend_others"):
            queryset = Friend.objects.filter((Q(user_source=suser) | Q(user_target=suser)) & Q(status=FriendStatus.ACCEPT))
            users = []
            for p in queryset:
                users.append(p.user_source.id)
                users.append(p.user_target.id)
                
            users = set(users)
            if suser in users:
                users.remove(suser)
            queryset = User.objects.filter(pk__in=users)
            
        elif self.action == "list_send":
            queryset = Friend.objects.filter(Q(user_source=self.request.user) & Q(status=FriendStatus.NEW))
        
        elif self.action == "list_wait":
            queryset = Friend.objects.filter(Q(user_target=self.request.user) & Q(status=FriendStatus.NEW))
            
        return queryset
    
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action in ('list_friend', 'list_friend_others'):
            serializer_class = UserSerializer
        return serializer_class
    
    def perform_create(self, serializer):
        serializer.save(
            user_source = self.request.user,
            user_target = get_object_or_404(User, pk=self.kwargs['user_id'])
        )
    
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user_target != self.request.user:
            raise FriendNotYourException
        if instance.status != FriendStatus.NEW:
            raise FriendAlreadyAcceptException
        
        serializer.save()
    
    def perform_destroy(self, instance):
        cuser = self.request.user
        if self.action == 'deny_friend_request':
            if instance.user_target != cuser:
                raise FriendNotYourException
            if instance.status != FriendStatus.NEW:
                raise FriendAlreadyDenyException
        if self.action == 'unfriend':
            if cuser not in (instance.user_source, instance.user_target):
                raise FriendAlreadyException
            if instance.status != FriendStatus.ACCEPT:
                raise FriendAlreadyException
        if self.action == 'cancel':
            if instance.user_source != cuser:
                raise FriendNotYourException
            if instance.status != FriendStatus.NEW:
                raise FriendAlreadyDenyException
        
        instance.delete()
        
    def deny_friend_request(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)
    
    def unfriend(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)
    
    def cancel(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)
        
    def list_friend(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
        
    def list_friend_others(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
        
    def list_send(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
        
    def list_wait(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
        
        
class UserFollowerViewSet(viewsets.ModelViewSet):
    serializer_class = UserFollowerSerializer
    
    def get_queryset(self):
        return UserFollower.objects.all()
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        if self.action == "list_follower":
            queryset = queryset.filter(user_target = self.request.user)
            users = [p.user_source.id for p in queryset]
            queryset = User.objects.filter(pk__in=users)
        elif self.action == "list_following":
            queryset = queryset.filter(user_source = self.request.user)
            users = [p.user_target.id for p in queryset]
            queryset = User.objects.filter(pk__in=users)
            
        return queryset
    
    def get_object(self):
        user_source = self.request.user.id
        user_target = self.kwargs.get('user_id', None)
        return get_object_or_404(self.get_queryset(), user_source=user_source, user_target=user_target)
        
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action in ('list_follower', 'list_following'):
            serializer_class = UserSerializer
        return serializer_class
        
    def create(self, request, *args, **kwargs):
        request.data['user_source'] = request.user.id
        request.data['user_target'] = self.kwargs['user_id']
        return super().create(request, *args, **kwargs)

    def list_follower(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def list_following(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        
     
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_auth(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)
     
        
friend_send_and_list_friend_others = FriendViewSet.as_view({'post': 'create', 'get': 'list_friend_others'})
friend_accept = FriendViewSet.as_view({'put': 'update'})
friend_deny = FriendViewSet.as_view({'delete': 'deny_friend_request'})
friend_unfriend = FriendViewSet.as_view({'delete': 'unfriend'})
friend_cancel = FriendViewSet.as_view({'delete': 'cancel'})
friend_list_friend = FriendViewSet.as_view({'get': 'list_friend'})
friend_list_send = FriendViewSet.as_view({'get': 'list_send'})
friend_list_wait = FriendViewSet.as_view({'get': 'list_wait'})

user_follower_list_follower = UserFollowerViewSet.as_view({'get': 'list_follower'})
user_follower_list_following = UserFollowerViewSet.as_view({'get': 'list_following'})
user_follower_create_destroy = UserFollowerViewSet.as_view({'post': 'create', 'delete': 'destroy'})
