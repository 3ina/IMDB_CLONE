from watchlist_app import models
from rest_framework import serializers

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Movie
        fields = ['__all__']



    def validate_name(self, value):
        pass
