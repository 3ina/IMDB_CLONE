from rest_framework.response import Response
from rest_framework.views import APIView
from watchlist_app.models import Movie
from watchlist_app.api.serializers import MovieSerializer
from django.http.request import HttpRequest


class MovieList(APIView):

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest):
        serializer = MovieSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


