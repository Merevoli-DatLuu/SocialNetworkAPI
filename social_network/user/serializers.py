from rest_framework import serializers

from .models import User
from .validators import validate_secure_email

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'password', 'age']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'password': {'required': True},
            'age': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            email       = validated_data['email'],
            first_name  = validated_data['first_name'],
            age         = validated_data['age']
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserVerifySerializer(serializers.Serializer):
    token = serializers.CharField(max_length=700)

    class Meta:
        model = User
        fields = ['token']

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_secure_email])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

class UserResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class UserResetConfirmPasswordSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_secure_email])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', )

