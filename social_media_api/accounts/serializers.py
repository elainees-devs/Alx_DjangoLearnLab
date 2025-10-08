from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    password2 = serializers.CharField(write_only=True, required=True)
    token = serializers.SerializerMethodField(read_only=True)
    extra_field = serializers.CharField(required=False)  # optional

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'token', 'extra_field'
        )

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Passwords didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')

        # explicitly call get_user_model() 
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        # explicitly use Token.objects.create 
        Token.objects.create(user=user)
        return user


    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key
    
class UserSerializer(serializers.ModelSerializer):
    """Serializer for full user details"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']


    
class FollowActionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class UserPublicSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'followers_count', 'following_count')
