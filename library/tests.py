from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from .models import Book


class BookAPITest(APITestCase):
    def setUp(self):
        # normal user
        self.user = User.objects.create_user(username='user', password='pass')
        self.token = Token.objects.create(user=self.user)

        # admin user
        self.admin = User.objects.create_superuser(
            username='admin', password='pass')
        self.admin_token = Token.objects.create(user=self.admin)

        # sample books
        Book.objects.create(title='Django for APIs',
                            author='William', genre='Tech', publication_year=2020)
        Book.objects.create(title='Learning Python',
                            author='Mark', genre='Tech', publication_year=2018)
        Book.objects.create(title='Mystery Novel', author='Jane',
                            genre='Fiction', publication_year=2015)

    def test_create_book_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            'title': 'New Book',
            'author': 'Author X',
            'genre': 'Sci-Fi',
            'publication_year': 2021,
        }
        resp = self.client.post('/api/books/', data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Book.objects.filter(title='New Book').count(), 1)

    def test_list_and_filter_books(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.get('/api/books/?author=William')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data['results']), 1)

    def test_search_by_title(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.get('/api/books/?search=Python')
        self.assertEqual(resp.status_code, 200)
        # should find 'Learning Python'
        titles = [b['title'] for b in resp.data['results']]
        self.assertIn('Learning Python', titles)

    def test_update_book(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        book = Book.objects.first()
        resp = self.client.patch(
            f'/api/books/{book.id}/', {'title': 'Updated Title'})
        self.assertEqual(resp.status_code, 200)
        book.refresh_from_db()
        self.assertEqual(book.title, 'Updated Title')

    def test_only_admin_can_delete(self):
        book = Book.objects.first()

        # non-admin attempt
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.delete(f'/api/books/{book.id}/')
        self.assertIn(resp.status_code, (403, 405))

        # admin attempt
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        resp = self.client.delete(f'/api/books/{book.id}/')
        self.assertEqual(resp.status_code, 204)
