from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.models import User


User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture']   
        read_only_fields = ['id']

    class RegisterSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True, required=True, validators=[validate_password] )
        password2 = serializers.CharField(write_only=True, required=True)

        class Meta:
            model = User
            fields = ['username', 'email', 'password', 'password2','first_name', 'last_name']

        def validate(self, attrs):
            if attrs.get['password'] != attrs['password2']:
                raise serializers.ValidationError({"password": "Password fields didn't match."})
            return attrs

        def create(self, validated_data):
            validated_data.pop('password2', None)
            password= validated_data.pop('password')
            user= User(**validated_data)
            user.set_password(password)
            user
            return user
      
