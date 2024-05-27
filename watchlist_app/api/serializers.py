from watchlist_app import models
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        exclude = ("watchlist")


class WatchListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    reviews = ReviewSerializer(many=True,read_only=True)
    len_name = serializers.SerializerMethodField()

    class Meta:
        model = models.WatchList
        fields = ['__all__']

    def get_len_name(self, obj):
        return len(obj.name)

    def validate(self, data):
        if data['title'] == data['description']:
            raise serializers.ValidationError("Title and Description should be different")
        else:
            return data

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is to short!")
        else:
            return value


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie-detail')

    class Meta:
        model = models.StreamPlatform
        fields = "__all__"
