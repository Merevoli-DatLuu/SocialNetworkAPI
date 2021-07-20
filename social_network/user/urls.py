from django.urls import path

from .views import UserRegisterView, UserLoginView, UserProfileView, UserDetailView, UserListView, UserChangePasswordView
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
    path('<int:user_id>',                               UserDetailView.as_view(),               name='other-user'),
    path('',                                            UserListView.as_view(),                 name='user-list'),
]