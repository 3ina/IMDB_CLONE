from rest_framework.test import APITestCase , APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import Token,RefreshToken

from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatformTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username="admin",
                                                        password="admin123",
                                                        email="admin@gmail.com",
                                                        is_staff=True)

        self.admin_token = self.get_token_for_user(self.admin_user)

        self.user = User.objects.create_user(username="test",
                                             password="password123",
                                             email="test@gmail.com")

        self.user_token = self.get_token_for_user(self.user)


        self.stream = models.StreamPlatform.objects.create(name="HBO",
                                                           about="#2 platform",
                                                           website="https://hbo.com")

    def get_token_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token)
        }
    def test_streamplatform_create_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.user_token['access'])
        data = {
            'name' : 'Netflix',
            'about' : '#11 streamming platform',
            'website' : "https://netflix.com"
        }

        response = self.client.post(reverse("streamplatform-list"),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

        def test_streamplatform_create_admin(self):
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access'])
            data = {
                'name': 'Netflix',
                'about': '#11 streamming platform',
                'website': "https://netflix.com"
            }

            response = self.client.post(reverse("streamplatform-list"), data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_stream_platform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        stream_platforms = models.StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformSerializer(stream_platforms,many=True)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,serializer.data)

    def test_get_stream_platform_detail(self):
        url = reverse('streamplatform-detail', args=[self.stream.id])
        response = self.client.get(url, format='json')
        stream_platform = models.StreamPlatform.objects.get(id=self.stream.id)
        serializer = serializers.StreamPlatformSerializer(stream_platform)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_stream_platform_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access'])
        url = reverse('streamplatform-detail', args=[self.stream.id])
        updated_data = {'name': 'Netflix', 'about': 'Updated about', 'website': 'https://www.netflix.com'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_stream_platform_as_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token['access'])
        url = reverse('streamplatform-detail', args=[self.stream.id])
        updated_data = {'name': 'Netflix', 'about': 'Updated about', 'website': 'https://www.netflix.com'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_stream_platform_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access'])
        url = reverse('streamplatform-detail', args=[self.stream.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_stream_platform_as_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token['access'])
        url = reverse('streamplatform-detail', args=[self.stream.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



