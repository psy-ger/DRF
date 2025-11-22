from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

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
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'genre', 'publication_year']
    search_fields = ['title']
    ordering_fields = ['publication_year', 'title']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        # set the creator user on creation
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        # ensure only admin can delete (permission class already checks object permission)
        return super().destroy(request, *args, **kwargs)


User = get_user_model()


class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        if not username or not password:
            return Response({'detail': 'username and password required'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'detail': 'username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            username=username, password=password, email=email)
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'username': user.username}, status=status.HTTP_201_CREATED)
