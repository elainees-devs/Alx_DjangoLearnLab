# posts/views.py
from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404, redirect
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .models import Post, Comment, Like
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.models import Notification

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

# -------------------------------
# Standalone view function
# -------------------------------
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get("content")
        if content:
            Comment.objects.create(
                author=request.user,
                post=post,
                content=content
            )
    return redirect('posts:post_detail', pk=post_id) 

# -------------------------------
# PostViewSet with TemplateHTMLRenderer
# -------------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = []
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]
    pagination_class = StandardResultsSetPagination
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "posts/post_list.html"

    def get_serializer_class(self):
        if self.action in ("list",):
            return PostListSerializer
        return PostDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return Response({'posts': serializer.data, 'user': request.user})
    
    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()              # actual model instance
        serializer = self.get_serializer(post)
        return Response({
        'post': post,                     # pass model instance for template
            'post_data': serializer.data,     # serialized data if needed
        'user': request.user
        })



    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    

# -------------------------------
# CommentViewSet
# -------------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["post", "author"]
    search_fields = ["content"]
    ordering_fields = ["created_at", "updated_at"]
    pagination_class = StandardResultsSetPagination
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "posts/comment_list.html"

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# -------------------------------
# FeedAPIView with TemplateHTMLRenderer
# -------------------------------
class FeedAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]  
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "posts/feed.html"

    def get_queryset(self):
        following_users = self.request.user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'posts': serializer.data})

# -------------------------------
# Like / Unlike
# -------------------------------
class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            Notification.objects.create(
                actor=request.user,
                recipient=post.author,
                verb='liked your post',
                target=post
            )
            return Response({'detail': 'Post liked'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(post=post, user=request.user)
        if like.exists():
            like.delete()
            return Response({'detail': 'Post unliked'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Not liked yet'}, status=status.HTTP_400_BAD_REQUEST)
