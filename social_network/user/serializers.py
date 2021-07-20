from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, PasswordChangeSerializer

from .models import User
from .validators import validate_secure_email, validate_age


class UserRegisterSerializer(RegisterSerializer):
    username = None
    age = serializers.IntegerField(validators=[validate_age], required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    
    def validate_password1(self, password):
        validate_secure_email(password)
        return super().validate_password1(password)
    
    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'age': self.validated_data.get('age', 0)
        }
    
    def save(self, request):
        user = super().save(request)
        user.age = self.data.get('age')
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.save()
        return user


class UserLoginSerializer(LoginSerializer):
    username = None


class UserChangePasswordSerializer(PasswordChangeSerializer):
    new_password1 = serializers.CharField(max_length=128, validators = [validate_secure_email])   


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', )

    
