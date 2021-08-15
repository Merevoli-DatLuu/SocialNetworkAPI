from django.urls import path

from .views import (UserRegisterView, UserLoginView, UserProfileView, 
                    UserDetailView, UserListView, UserChangePasswordView,
                    friend_send_and_list_friend_others, friend_accept, friend_deny,
                    friend_unfriend, friend_cancel, friend_list_friend,
                    friend_list_send, friend_list_wait, user_follower_create_destroy,
                    user_follower_list_following, user_follower_list_follower)
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView

urlpatterns = [
    path('register',                                    UserRegisterView.as_view(),             name='register'),
    path('verify-user',                                 VerifyEmailView.as_view(),              name='verify-user'),
    path('login',                                       UserLoginView.as_view(),                name='login'),
    path('change-password',                             UserChangePasswordView.as_view(),       name='change-password'),
    path('reset-password',                              PasswordResetView.as_view(),            name='reset-password'),
    path('reset-confirm-password/<uidb64>/<token>/',    PasswordResetConfirmView.as_view(),     name='password_reset_confirm'),
    path('me',                                          UserProfileView.as_view(),              name='current-user'),
    path('',                                            UserListView.as_view(),                 name='user-list'),
    path('<int:user_id>',                               UserDetailView.as_view(),               name='other-user'),
    path('friend/<int:user_id>',                        friend_send_and_list_friend_others,     name='friend-send-and-list-friend-others'),
    path('friend/<int:pk>/accept',                      friend_accept,                          name='friend-accept'),
    path('friend/<int:pk>/deny',                        friend_deny,                            name='friend-deny'),
    path('friend/<int:pk>/cancel',                      friend_cancel,                          name='friend-unfriend'),
    path('friend/<int:pk>/unfriend',                    friend_unfriend,                        name='friend-cancel'),
    path('friend/',                                     friend_list_friend,                     name='friend-list-friend'),
    path('friend/list-send',                            friend_list_send,                       name='friend-list-send'),
    path('friend/list-wait',                            friend_list_wait,                       name='friend-list-wait'),
    path('follower/<int:user_id>',                      user_follower_create_destroy,           name='user-follower-create-destroy'),
    path('follower/list-follower',                      user_follower_list_follower,            name='user-follower-list-follower'),
    path('follower/list-following',                     user_follower_list_following,           name='user-follower-list-following'),
]