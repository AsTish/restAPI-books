from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from myapp.models import Author

# Create your tests here.

class AuthorCreateViewTest(APITestCase):

    def setUp(self):
        self.valid_author_data = {
            "name": "Ray Bradbury",
            "birth_date": "1920-08-22",
            "nationality": "American"
        }
        self.existing_author = Author.objects.create(
            name="Joanne Rowling",
            birth_date="1965-07-31",
            nationality="British"
        )

    def test_create_author_successful(self):
        url = reverse('create-author')
        data = self.valid_author_data
        response = self.client.post(url, data)
        print(response.data)  # Отладочный вывод для проверки ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_create_existing_author_failure(self):
        url = reverse('create-author')  # Убедитесь, что имя маршрута соответствует вашему urls.py
        response = self.client.post(url, {
            "name": "Joanne Rowling",
            "birth_date": "1965-07-31",
            "nationality": "British"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], "An author with this name and birth date already exists.")
        self.assertEqual(Author.objects.count(), 1)  # Убедитесь, что количество авторов не изменилось