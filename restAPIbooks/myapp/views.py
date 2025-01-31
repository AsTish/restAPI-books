from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError

from myapp.models import Author, Book
from myapp.serializers import AuthorSerializer, BookSerializer

# Create your views here.
class AuthorCreateView(CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if Author.objects.filter(name=data.get('name'), birth_date=data.get('birth_date')).exists():
            raise ValidationError(
                {"detail": "An author with this name and birth date already exists."}
            )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                "message": f"Author '{serializer.data['name']}' created successfully!",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


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


class AuthorDetailView(RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        return super().get_queryset()

    def handle_exception(self, exc):
        """
        Перехватываем исключения, чтобы возвращать более понятный ответ, если автор не найден.
        """
        if isinstance(exc, NotFound):
            return Response(
                {"detail": "Author with the specified ID not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        return super().handle_exception(exc)


class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        title = data.get('title')
        author_id = data.get('author')  # Убедитесь, что поле 'author' передается в запросе

        # # Проверяем наличие книги с таким же названием и автором
        # if Book.objects.filter(title=title, author_id=author_id).exists():
        #     raise ValidationError(
        #         {"detail": f"A book with the title '{title}' already exists for this author."}
        #     )

        data = request.data
        if Book.objects.filter(title=data.get('title'), author_id=data.get('author_id')).exists():
            raise ValidationError(
                {"detail": f"A book with the title '{title}' already exists for this author."}
            )

        return super().create(request, *args, **kwargs)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {
                "message": f"Book '{serializer.data.get('title')}' created successfully!",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )



class BooksListView(ListAPIView):
    queryset = Book.objects.all().order_by('-publication_date', 'title')    # Сортировка по умолчанию
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]    # Подключение фильтрации и сортировки
    filterset_fields = ['author', 'genre', 'publication_date']    # Поля для фильтрации
    ordering_fields = ['author', 'title', 'publication_date', 'genre']    # Поля для сортировки
    ordering = ['-publication_date', 'title']    # Сортировка по умолчанию

    def get_queryset(self):
        queryset = super().get_queryset()
        # Можно добавить кастомные фильтры, если потребуется
        return queryset


class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Фильтруем книги, которые только активны (например, без удаленных)"""
        return super().get_queryset()  # Расширите, если нужны условия

    def get_object(self):
        """Переопределение для кастомного сообщения об ошибке, если объект не найден"""
        try:
            return super().get_object()
        except Book.DoesNotExist:
            raise NotFound({"detail": "Book with the specified ID not found"})


class BookDeleteView(DestroyAPIView):
    queryset = Book.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            book_id = kwargs.get('id')  # Получаем ID книги из URL
            book = self.get_queryset().get(id=book_id)  # Пытаемся найти книгу
        except Book.DoesNotExist:
            raise NotFound({"detail": f"Book with ID '{book_id}' not found."})

        # Удаляем книгу
        book.delete()
        return Response(
            {"message": f"Book with ID '{book_id}' deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class AuthorDeleteView(DestroyAPIView):
    queryset = Author.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            author_id = kwargs.get('id')  # Получаем ID автора из URL
            author = self.get_queryset().get(id=author_id)  # Пытаемся найти автора
        except Author.DoesNotExist:
            raise NotFound({"detail": f"Author with id '{author_id} not found."})

        # Удаляем автора (и связанные книги автоматически)
        author.delete()
        return Response(
            {"message": f"Author '{author}' and all author's books deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'  # Поле для поиска книги

    def update(self, request, *args, **kwargs):
        try:
            # Получаем объект книги
            book_id = kwargs.get('id')
            book = self.get_queryset().get(id=book_id)
        except Book.DoesNotExist:
            raise NotFound({"detail": f"Book with ID '{book_id}' not found."})

        # Выполняем обновление с помощью сериализатора
        partial = kwargs.pop('partial', False)  # Проверяем, является ли запрос частичным (PATCH)
        serializer = self.get_serializer(book, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "message": f"Book with ID '{book_id}' updated successfully!",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )


# test