from rest_framework.serializers import (
    ModelSerializer,
    UUIDField,
    StringRelatedField,
    SerializerMethodField,
    ValidationError,
    DateField
)
from myapp.models import Author, Book

class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'birth_date', 'nationality']  # Укажите поля, которые должны быть включены в сериализатор

    def validate_name(self, value):
        """Проверка, чтобы имя не было пустым."""
        if not value:
            raise ValidationError("Name field cannot be empty.")
        return value

    def validate(self, data):
        name = data.get('name')
        birth_date = data.get('birth_date')
        if Author.objects.filter(name=name, birth_date=birth_date).exists():
            raise ValidationError("An author with this name and birth date already exists.")
        return data


# class BookSerializer(ModelSerializer):
#     # Дополняем поле author, чтобы вводился только текст
#     author = CharField(write_only=True, help_text="Enter the author's name.")
#     author_id = PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Book
#         fields = ['id', 'title', 'author', 'author_id', 'publication_date', 'genre']

#     def validate_author(self, value):
#         """Валидация автора: проверка имени на корректность"""
#         if not value.strip():
#             raise ValidationError("Author name cannot be empty.")
#         return value.strip()

#     def create(self, validated_data):
#         """Обработка создания книги с текстовым вводом автора"""
#         author_name = validated_data.pop('author')  # Убираем 'author' из входных данных
#         author, created = Author.objects.get_or_create(name=author_name)
#         return Book.objects.create(author=author, **validated_data)


class BookSerializer(ModelSerializer):
    author_id = UUIDField(
        write_only=True,
        help_text="Provide the UUID of the author."
    )
    author = StringRelatedField(read_only=True)
    # available_authors = SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author_id', 'author', 'publication_date', 'genre']

    # def get_available_authors(self, obj):
    #     """Возвращает список доступных авторов"""
    #     authors = Author.objects.all()
    #     return [{'id': author.id, 'name': str(author)} for author in authors]

    def validate_author_id(self, value):
        """Проверка, что указанный author_id существует"""
        if not Author.objects.filter(id=value).exists():
            raise ValidationError("Author with the provided ID does not exist.")
        return value

    def create(self, validated_data):
        """Создание книги с использованием author_id"""
        author_id = validated_data.pop('author_id')
        author = Author.objects.get(id=author_id)
        return Book.objects.create(author=author, **validated_data)