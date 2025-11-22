from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre',
                  'publication_year', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']
