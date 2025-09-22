# api/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Author, Book

class BookAPITest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Ngugi wa Thiong'o")
        self.book = Book.objects.create(title="The River Between", publication_year=1965, author=self.author)

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        url = reverse("book-list")
        data = {"title": "Devil on the Cross", "publication_year": 1980, "author": self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # requires auth

    def test_retrieve_book(self):
        url = reverse("book-detail", args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "The River Between")

    def test_ordering(self):
        url = reverse("book-list") + "?ordering=-publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
