# posts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")  # extend as needed (email, first_name)

class CommentSerializer(serializers.ModelSerializer):
    author = UserBasicSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ("id", "post", "author", "content", "created_at", "updated_at")
        read_only_fields = ("id", "author", "created_at", "updated_at")

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["author"] = request.user
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    author = UserBasicSerializer(read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "author", "content", "created_at", "updated_at", "comments_count")


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserBasicSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "author", "content", "created_at", "updated_at", "comments")
        read_only_fields = ("id", "author", "created_at", "updated_at", "comments")
