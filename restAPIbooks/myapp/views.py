from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import status

from myapp.models import Author, Book
from myapp.serializers import AuthorSerializer, BookSerializer

# Create your views here.
class AuthorCreateView(CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorsListView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name', 'birth_date']
    ordering_fields = ['name', 'birth_date']
    ordering = ['name', '-birth_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Можно добавить кастомные фильтры, если потребуется
        return queryset


class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "message": f"Book '{serializer.data.get('title')}' created successfully!",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class BooksListView(ListAPIView):
    queryset = Book.objects.all().order_by('author', 'title')    # Сортировка по умолчанию
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]    # Подключение фильтрации и сортировки
    filterset_fields = ['author', 'genre', 'publication_date']    # Поля для фильтрации
    ordering_fields = ['author', 'title', 'publication_date', 'genre']    # Поля для сортировки
    ordering = ['author', 'title']    # Сортировка по умолчанию

    def get_queryset(self):
        queryset = super().get_queryset()
        # Можно добавить кастомные фильтры, если потребуется
        return queryset