from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from myapp.models import Author, Book

# Create your tests here.

class AuthorCreateViewTest(APITestCase):
    """
    Тесты для проверки функциональности представления AuthorCreateView.
    """

    def setUp(self):
        """
        Настройка тестовых данных перед выполнением каждого теста.
        """
        self.valid_author_data = {
            "name": "Ray Bradbury",  # Уникальные данные для успешного теста
            "birth_date": "1920-08-22",
            "nationality": "American"
        }
        self.existing_author = Author.objects.create(
            name="Joanne Rowling",  # Уже существующий автор для проверки дублирования
            birth_date="1965-07-31",
            nationality="British"
        )

    def test_create_author_successful(self):
        """
        Проверяет успешное создание автора с уникальными данными.
        """
        url = reverse('create-author')  # Маршрут для создания автора
        data = self.valid_author_data  # Данные для запроса
        response = self.client.post(url, data)  # Отправка POST-запроса

        # Проверка, что запрос завершился с кодом 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверка, что автор действительно добавлен в базу данных
        self.assertEqual(Author.objects.count(), 2)

    def test_create_existing_author_failure(self):
        """
        Проверяет ошибку при попытке создать автора с уже существующими данными.
        """
        url = reverse('create-author')  # Маршрут для создания автора
        response = self.client.post(url, {  # Дублирующие данные
            "name": "Joanne Rowling",
            "birth_date": "1965-07-31",
            "nationality": "British"
        })

        # Проверка, что запрос завершился с кодом 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверка, что в ответе присутствует ключ 'detail' с описанием ошибки
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], "An author with this name and birth date already exists.")

        # Убедитесь, что количество авторов в базе не изменилось
        self.assertEqual(Author.objects.count(), 1)


class BookCreateViewTest(APITestCase):
    """
    Тесты для проверки функциональности представления BookCreateView.
    """

    def setUp(self):
        """
        Настройка тестовых данных перед выполнением каждого теста.
        """
        self.author = Author.objects.create(
            name="Ray Bradbury",
            birth_date="1920-08-22",
            nationality="American"
        )
        self.valid_book_data = {
            "title": "Fahrenheit 451",  # Уникальные данные для успешного теста
            "author_id": str(self.author.id),
            "publication_date": "1953-10-19",
            "genre": "Dystopian"
        }
        self.existing_book = Book.objects.create(
            title="Fahrenheit 451",  # Уже существующая книга
            author=self.author,
            publication_date="1953-10-19",
            genre="Dystopian"
        )

    def test_create_book_successful(self):
        """
        Проверяет успешное создание книги с уникальными данными.
        """
        url = reverse('create-book')  # Убедитесь, что маршрут соответствует вашему urls.py
        data = {
            "title": "The Martian Chronicles",
            "author_id": str(self.author.id),  # Используется author_id
            "publication_date": "1950-05-03",
            "genre": "Science Fiction"
        }
        response = self.client.post(url, data)
        print(response.data)  # Отладочный вывод данных ответа (можно убрать после проверки)

        # Проверка, что запрос завершился с кодом 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверка, что книга действительно добавлена в базу данных
        self.assertEqual(Book.objects.count(), 2)

    def test_create_existing_book_failure(self):
        """
        Проверяет ошибку при попытке создать книгу с уже существующими данными.
        """
        url = reverse('create-book')  # Убедитесь, что маршрут соответствует вашему urls.py
        data = {
            "title": "Fahrenheit 451",
            "author_id": str(self.author.id),  # Используется author_id
            "publication_date": "1953-10-19",
            "genre": "Dystopian"
        }
        response = self.client.post(url, data)

        # Проверка, что запрос завершился с кодом 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверка, что в ответе присутствует ключ 'detail' с описанием ошибки
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], f"A book with the title '{data["title"]}' already exists for this author.")

        # Убедитесь, что количество книг в базе не изменилось
        self.assertEqual(Book.objects.count(), 1)