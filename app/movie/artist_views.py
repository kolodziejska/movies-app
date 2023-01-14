"""
Views for movie/artist API.
"""

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from django.utils.text import slugify

from core.models import Movie, Genre, Artist
from core.permissions import IsAdmin
from movie import serializers


class RetrieveArtistView(generics.RetrieveAPIView):

    serializer_class = serializers.ArtistSerializer
    queryset = Artist.objects.all()
    lookup_field = "slug"

    def retrieve(self, request, slug):
        """Override retrieve method to retrieve artist with movies."""

        # retrieve artist
        instance = self.get_object()
        artist_serializer = self.get_serializer(instance)

        # retrieve directed movies
        directed = Movie.objects.filter(director=instance.id)
        directed_serializer = serializers.BasicMovieSerializer(directed, many=True)

        # retrieve starred movies
        starred = Movie.objects.filter(actors=instance.id)
        starred_serializer = serializers.BasicMovieSerializer(starred, many=True)

        data = artist_serializer.data
        data['Directed'] = directed_serializer.data
        data['Starred'] = starred_serializer.data

        return Response(data)

class CreateArtistView(generics.CreateAPIView):

    serializer_class = serializers.ArtistSerializer
    permission_classes = [IsAdmin]
    authentication_classes = [TokenAuthentication]

    def create(self, request):
        """Override create method to autogenerate a slug."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        if not instance.slug:
            slug_artist = f"{instance.first_name} {instance.last_name} {instance.id}"
            instance.slug = slugify(slug_artist)
            instance.save()
        
        return Response(serializer.data, status=200)

