from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from datetime import datetime

from myapp.models import Author, Book

# Create your tests here.

class AuthorCreateViewTest(APITestCase):
    """
    Тесты для проверки функциональности представления AuthorCreateView.
    """

    def setUp(self):
        """
        Настройка тестовых данных.
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
        Настройка тестовых данных.
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


class BookDeleteViewTest(APITestCase):
    """
    Тесты для проверки функциональности представления BookDeleteView.
    """

    def setUp(self):
        """
        Настройка тестовых данных.
        """
        self.author = Author.objects.create(
            name="Ray Bradbury",
            birth_date="1920-08-22",
            nationality="American"
        )
        self.book = Book.objects.create(
            title="Fahrenheit 451",
            author=self.author,
            publication_date="1953-10-19",
            genre="Dystopian"
        )

    def test_delete_book_successful(self):
        """
        Проверяет успешное удаление существующей книги.
        """
        url = reverse('delete-book', kwargs={'id': str(self.book.id)})
        response = self.client.delete(url)

        # Проверка, что запрос завершился с кодом 204 (No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверка, что книга была удалена из базы данных
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_delete_nonexistent_book(self):
        """
        Проверяет, что удаление несуществующей книги возвращает ошибку 404.
        """
        non_existent_id = "123e4567-e89b-12d3-a456-426614174000"  # Несуществующий UUID
        url = reverse('delete-book', kwargs={'id': non_existent_id})
        response = self.client.delete(url)

        # Проверка, что запрос завершился с кодом 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Проверка сообщения об ошибке
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], f"Book with ID '{non_existent_id}' not found.")


class AuthorDeleteViewTest(APITestCase):
    """
    Тесты для проверки функциональности представления AuthorDeleteView.
    """

    def setUp(self):
        """
        Настройка тестовых данных.
        """
        self.author = Author.objects.create(
            name="Ray Bradbury",
            birth_date="1920-08-22",
            nationality="American"
        )
        self.book1 = Book.objects.create(
            title="Fahrenheit 451",
            author=self.author,
            publication_date="1953-10-19",
            genre="Dystopian"
        )
        self.book2 = Book.objects.create(
            title="The Martian Chronicles",
            author=self.author,
            publication_date="1950-05-03",
            genre="Science Fiction"
        )

    def test_delete_author_successful(self):
        """
        Проверяет успешное удаление автора и всех связанных с ним книг.
        """
        url = reverse('delete-author', kwargs={'id': str(self.author.id)})  # Убедитесь, что маршрут соответствует вашему urls.py
        response = self.client.delete(url)

        # Проверка, что запрос завершился с кодом 204 (No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверка, что автор был удалён из базы данных
        self.assertFalse(Author.objects.filter(id=self.author.id).exists())

        # Проверка, что связанные книги были удалены
        self.assertFalse(Book.objects.filter(author=self.author).exists())

        # Проверка ссобщения об успешном удалении
        self.assertEqual(response.data['message'], f"Author '{self.author.name}' and all author's books deleted successfully.")

    def test_delete_nonexistent_author(self):
        """
        Проверяет, что удаление несуществующего автора возвращает ошибку 404.
        """
        non_existent_id = "123e4567-e89b-12d3-a456-426614174000"  # Несуществующий UUID
        url = reverse('delete-author', kwargs={'id': non_existent_id})
        response = self.client.delete(url)

        # Проверка, что запрос завершился с кодом 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Проверка сообщения об ошибке
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], f"Author with id '{non_existent_id} not found.")


class BookUpdateViewTest(APITestCase):
    """
    Тесты для проверки функциональности представления BookUpdateView.
    """

    def setUp(self):
        """
        Настройка тестовых данных.
        """
        self.author = Author.objects.create(
            name="Ray Bradbury",
            birth_date="1920-08-22",
            nationality="American"
        )
        self.book = Book.objects.create(
            title="Fahrenheit 451",
            author=self.author,
            publication_date="1953-10-19",
            genre="Dystopian"
        )
        self.valid_book_data = {
            "title": "Fahrenheit 451 Updated",
            "author_id": str(self.author.id),
            "publication_date": "1953-10-20",
            "genre": "Science Fiction"
        }

    def test_update_book_successful(self):
        """
        Проверяет успешное обновление данных книги.
        """
        url = reverse('update-book', kwargs={'id': str(self.book.id)})  # Убедитесь, что маршрут соответствует вашему urls.py
        response = self.client.put(url, self.valid_book_data)

        # Проверка, что запрос завершился с кодом 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка, что данные книги были обновлены
        self.book.refresh_from_db()  # Перезагружаем книгу из базы данных
        self.assertEqual(self.book.title, self.valid_book_data['title'])
    
        # Преобразуем строку даты в datetime.date для сравнения
        expected_date = datetime.strptime(self.valid_book_data['publication_date'], "%Y-%m-%d").date()
        self.assertEqual(self.book.publication_date, expected_date)

        self.assertEqual(self.book.genre, self.valid_book_data['genre'])

        # Проверка, что ответ содержит правильные данные
        self.assertEqual(response.data['message'], f"Book with ID '{self.book.id}' updated successfully!")
        self.assertEqual(response.data['data']['title'], self.valid_book_data['title'])

    def test_update_nonexistent_book(self):
        """
        Проверяет, что обновление несуществующей книги возвращает ошибку 404.
        """
        non_existent_id = "123e4567-e89b-12d3-a456-426614174000"  # Несуществующий UUID
        url = reverse('update-book', kwargs={'id': non_existent_id})
        response = self.client.put(url, self.valid_book_data)

        # Проверка, что запрос завершился с кодом 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Проверка сообщения об ошибке
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], f"Book with ID '{non_existent_id}' not found.")


# test
# test 2
# test 3
# test 4
# test 5
# test 6