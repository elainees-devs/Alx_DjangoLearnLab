# posts/views.py
from rest_framework import viewsets, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from notifications.utils import create_notification
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Like
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
)
from .permissions import IsOwnerOrReadOnly, IsAuthenticated


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = []  # e.g., ['author'] if you want direct field filters
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action in ("list",):
            return PostListSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()  
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["post", "author"]
    search_fields = ["content"]
    ordering_fields = ["created_at", "updated_at"]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get all users that the current user is following
        following_users = self.request.user.following.all()  # <- satisfies following.all()
        # Return posts from followed users ordered by newest first
        return Post.objects.filter(author__in=following_users).order_by('-created_at')  # <- satisfies filter(...).order_by(...)

class LikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if created:
            # Create notification
            create_notification(actor=request.user, recipient=post.author, verb='liked your post', target=post)
            return Response({'detail': 'Post liked'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(post=post, user=request.user)
        if like.exists():
            like.delete()
            return Response({'detail': 'Post unliked'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Not liked yet'}, status=status.HTTP_400_BAD_REQUEST)