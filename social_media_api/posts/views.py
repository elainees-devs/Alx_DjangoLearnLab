# posts/views.py
from rest_framework import viewsets, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Comment
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
)
from .permissions import IsOwnerOrReadOnly

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
