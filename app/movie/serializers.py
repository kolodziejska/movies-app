"""
Serializers for movie API
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models import Movie, Genre, Rating, Artist
from user.serializers import BasicUserSerializer


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for genre object"""
    
    class Meta:
        model = Genre
        fields = ['genre']


class ArtistSerializer(serializers.ModelSerializer):
    """Serializer for artist object"""

    class Meta:
        model = Artist
        fields = ['first_name', 'last_name']


class BasicMovieSerializer(serializers.ModelSerializer):
    """Basic movie serializer for listing movies."""

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'average_rating']
        read_only_fields = ['id', 'average_rating']


class MovieSerializer(BasicMovieSerializer):
    """Serializer for movie object"""

    genre = GenreSerializer(read_only=True, many=True)
    director = ArtistSerializer(read_only=True, many=True)
    actors = ArtistSerializer(read_only=True, many=True)

    class Meta(BasicMovieSerializer.Meta):
        model = Movie
        fields = BasicMovieSerializer.Meta.fields + \
                 [
                  'genre',
                  'director',
                  'actors',
                  'overview',
                  'created',
                  'updated']
        read_only_fields = BasicMovieSerializer.Meta.read_only_fields + \
                 ['created', 'updated']


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for listing ratings in movie view."""

    user = BasicUserSerializer()

    class Meta:
        model = Rating
        fields = ['id', 'rating', 'user', 'comment']
        read_only_fields = ['id', 'user']


class ManageRatingSerializer(serializers.ModelSerializer):
    """Serializer for adding and editing rating."""

    class Meta:
        model = Rating
        fields = ['id', 'movie_id', 'user', 'rating', 'comment']
        read_only_fields = ['id']

