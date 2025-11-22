from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer


class IsAdminOrReadDeleteOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only admins can delete; other actions allowed for authenticated users
        if request.method == 'DELETE':
            return request.user.is_staff
        return True


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadDeleteOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author', 'genre', 'publication_year']
    search_fields = ['title']

    def destroy(self, request, *args, **kwargs):
        # ensure only admin can delete (permission class already checks object permission)
        return super().destroy(request, *args, **kwargs)
