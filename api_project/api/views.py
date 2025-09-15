# api/views.py
from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can view



# ViewSet for full CRUD
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  
    # Authenticated → full CRUD
    # Unauthenticated → read-only (GET)