from django.http import Http404

from rest_framework.generics import RetrieveAPIView, ListAPIView
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, PasswordChangeView

from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, UserChangePasswordSerializer
from .models import User
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
