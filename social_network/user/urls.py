from django.urls import path

from .views import UserRegisterView, UserResetConfirmPasswordView, UserVerifyView, UserLoginView, UserChangePasswordView, UserResetPasswordView, UserProfileView, UserDetailView, UserListView

urlpatterns = [
    path('register',                UserRegisterView.as_view(),             name='register'),
    path('verify-user',             UserVerifyView.as_view(),               name='verify-user'),
    path('login',                   UserLoginView.as_view(),                name='login'),
    path('change-password',         UserChangePasswordView.as_view(),       name='change-password'),
    path('reset-password',          UserResetPasswordView.as_view(),        name='reset-password'),
    path('reset-confirm-password',  UserResetConfirmPasswordView.as_view(), name='reset-confirm-password'),
    path('me',                      UserProfileView.as_view(),              name='current-user'),
    path('<int:user_id>',           UserDetailView.as_view(),               name='orther-user'),
    path('',                        UserListView.as_view(),                 name='user-list'),
]