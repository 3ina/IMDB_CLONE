import json

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



class WatchListViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpassword',
            is_staff=True,
            email="admin@gmail.com",
        )

        self.admin_token = self.get_token_for_user(self.admin_user)

        self.user = User.objects.create_user(
            username='user',
            password='userpassword',
            email="user@gmail.com",

        )

        self.user_token = self.get_token_for_user(self.user)
        self.stream = models.StreamPlatform.objects.create(name="HBO",
                                                           about="#2 platform",
                                                           website="https://hbo.com")

        self.watchlist_data = {'title': 'Inception', 'storyline': 'A mind-bending thriller', 'platform':self.stream.id}
        self.watchlist = models.WatchList.objects.create(title='Inception',storyline='A mind-bending thriller',platform=self.stream)
        self.url = reverse('movie-list')

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def test_get_watchlist(self):
        response = self.client.get(self.url, format='json')
        watchlists = models.WatchList.objects.all()
        serializer = serializers.WatchListSerializer(watchlists, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_watchlist_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token['access'])
        response = self.client.post(self.url, self.watchlist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_watchlist_as_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token['access'])
        response = self.client.post(self.url, self.watchlist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_watchlist_without_auth(self):
        response = self.client.post(self.url, self.watchlist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class ReviewCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', password='testpass',email="test@gmail.com")
        self.client = APIClient()
        self.platform = models.StreamPlatform.objects.create(name="Netflix", about="Stream movies",
                                                      website="https://netflix.com")
        self.watchlist = models.WatchList.objects.create(title="Example Movie", storyline="An example storyline",
                                                  platform=self.platform)

    def authenticate(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_review(self):
        self.authenticate()
        data = {
            "rating": 5,
            "description": "Great movie!",
            "watchlist": self.watchlist.id
        }
        response = self.client.post(reverse('review-create', kwargs={'pk': self.watchlist.id}), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_duplicate_review(self):
        self.authenticate()
        data = {
            "rating": 5,
            "description": "Great movie!",
            "watchlist": self.watchlist.id
        }
        self.client.post(reverse('review-create', kwargs={'pk': self.watchlist.id}), data)
        response = self.client.post(reverse('review-create', kwargs={'pk': self.watchlist.id}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReviewDetailTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        self.client = APIClient()
        self.platform = models.StreamPlatform.objects.create(name="Netflix", about="Stream movies",
                                                      website="https://netflix.com")
        self.watchlist = models.WatchList.objects.create(title="Example Movie", storyline="An example storyline",
                                                  platform=self.platform)
        self.review = models.Review.objects.create(user=self.user, rating=5, description="Great movie!",
                                            watchlist=self.watchlist)

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_review(self):
        response = self.client.get(reverse('review-detail', kwargs={'pk': self.review.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_review(self):
        self.authenticate(self.user)
        data = {
            "rating": 4,
            "description": "Updated review",
        }
        response = self.client.put(reverse('review-detail', kwargs={'pk': self.review.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.description, "Updated review")

    def test_update_review_by_other_user(self):
        self.authenticate(self.user2)
        data = {
            "rating": 4,
            "description": "Updated review",
        }
        response = self.client.put(reverse('review-detail', kwargs={'pk': self.review.id}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review(self):
        self.authenticate(self.user)
        response = self.client.delete(reverse('review-detail', kwargs={'pk': self.review.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_review_by_other_user(self):
        self.authenticate(self.user2)
        response = self.client.delete(reverse('review-detail', kwargs={'pk': self.review.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)