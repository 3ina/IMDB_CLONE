from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import Token


class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            "username": "testcase",
            "email": "testcase@gmail.com",
            "password": "password",
            "password2": "password",

        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "username": "testcase",
            "email": "testcase@gmail.com",
            "password": "password",

        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test",
            email="test@gmail.com",
            password="test2024"
        )


class TokenTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token_obtain_url = reverse('token_obtain_view')
        self.token_refresh_url = reverse('token_refresh_view')

    def test_token_obtain_pair(self):
        response = self.client.post(self.token_obtain_url, {'username': 'testuser', 'password': 'testpassword'},
                                    format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_obtain_pair_invalid_credentials(self):
        response = self.client.post(self.token_obtain_url, {'username': 'testuser', 'password': 'wrongpassword'},
                                    format='json')
        self.assertEqual(response.status_code, 401)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    def test_token_refresh(self):
        response = self.client.post(self.token_obtain_url, {'username': 'testuser', 'password': 'testpassword'},
                                    format='json')
        refresh_token = response.data['refresh']

        # Refresh the access token
        response = self.client.post(self.token_refresh_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_token_refresh_invalid_token(self):
        response = self.client.post(self.token_refresh_url, {'refresh': 'invalidtoken'}, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertNotIn('access', response.data)
