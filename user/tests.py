from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            "username" : "testcase",
            "email" : "testcase@gmail.com",
            "password" : "password",
            "password2": "password",

        }

        response = self.client.post(reverse('register'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        data = {
            "username": "testcase",
            "email": "testcase@gmail.com",
            "password": "password",


        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

