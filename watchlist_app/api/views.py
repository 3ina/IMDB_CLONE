import rest_framework.serializers
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import (
    WatchListSerializer, StreamPlatformSerializer, ReviewSerializer , ReviewCreateSerializer
)
from django.http.request import HttpRequest
from rest_framework import mixins, generics ,viewsets
from .permissions import AdminOrReadOnly , ReviewUserOrReadOnly
from rest_framework.permissions import IsAuthenticated


from .pagination import WatchListPagination


class UserReview(generics.ListAPIView):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return Review.objects.filter(user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer :rest_framework.serializers.Serializer):

        if getattr(self, 'swagger_fake_view', False):
            return

        pk = self.kwargs.get('pk')
        watchList = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchList,user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")

        if watchList.number_rating == 0:
            watchList.avg_rating = serializer.validated_data['rating']
        else:
            watchList.avg_rating = (watchList.avg_rating + serializer.validated_data['rating'])/2

        watchList.number_rating = watchList.number_rating + 1
        watchList.save()
        Review.objects.create(
            user=review_user,
            rating=serializer.validated_data['rating'],
            description=serializer.validated_data['description'],
            watchlist=watchList,
        )

    def get_queryset(self):
        return Review.objects.all()


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]




class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__username','active']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist_id=pk)


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [AdminOrReadOnly]


class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListPagination



class StreamPlatformList(APIView):

    def get(self, request: HttpRequest):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True, context={'request', request})
        return Response(serializer.data)

    def post(self, request: HttpRequest):
        serializer = StreamPlatformSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamPlatformDetail(APIView):
    def get(self, request, pk):
        try:
            stream = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"error": "stream platform does not exists"})

        serializer = StreamPlatformSerializer(stream)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            stream = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"error": "stream platform does not exists"})

        serializer = StreamPlatformSerializer(stream, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        try:
            stream = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"error": "stream platform does not exists"})

        stream.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListV(APIView):


    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)


    def post(self, request: HttpRequest):
        self.permission_classes = [AdminOrReadOnly]
        self.check_permissions(request)
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class WatchDetail(APIView):

    def get(self, request: HttpRequest, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'movie not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request: HttpRequest, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'movie not found'}, status=status.HTTP_404_NOT_FOUND)

        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



