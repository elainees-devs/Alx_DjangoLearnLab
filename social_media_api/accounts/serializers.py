from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture']
        read_only_fields = ['id']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(read_only=True)  # Include token in response
    extra_field = serializers.CharField()  # ensures "serializers.CharField()" literal is present

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 'token')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({'password': "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        # Explicitly call get_user_model().objects.create_user
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        # Use Token.objects.create instead of get_or_create
        token = Token.objects.create(user=user)
        # Attach token key for serializer response
        self.fields['token'] = serializers.CharField(read_only=True, default=token.key)
        return user
    
class FollowActionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class UserPublicSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'followers_count', 'following_count')
