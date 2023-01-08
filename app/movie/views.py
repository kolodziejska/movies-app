"""
Views for movie API.
"""

from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from core.models import Movie, Genre, Artist, Rating
from core.permissions import IsAdminOrReadOnly
from movie import serializers


class MovieViewSet(viewsets.ModelViewSet):
    """View for manage movie APIs."""
    serializer_class = serializers.MovieSerializer
    queryset = Movie.objects.all()
    http_method_names = ['get', 'post']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """Retrieve movies with filtering and ordering."""
        queryset = self.queryset
        ordering_field = '-average_rating'
        # filtering by title:
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__istartswith=title)
        
        # filtering by genre:
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre__genre=genre)

        # check ordering:
        new_ordering = self.request.query_params.get('order_by')
        if new_ordering == 'rating':
            ordering_field = '-average_rating'
        elif new_ordering == 'title':
            ordering_field = 'title'
        return queryset.order_by(ordering_field)
    
    def retrieve(self, request, pk):
        """Override retrieve method to retrieve movie with ratings."""

        # retrieve movie
        instance = self.get_object()
        movie_serializer = self.get_serializer(instance)

        # retrieve ratings
        ratings = Rating.objects.filter(movie_id=pk)
        ratings_serializer = serializers.RatingSerializer(ratings, many=True)

        data = movie_serializer.data
        data['Ratings'] = ratings_serializer.data

        return Response(data)
    
    @action(
        methods=['post'],
        detail=True,
        url_path='add_rating',
        authentication_classes = [TokenAuthentication],
        permission_classes = [IsAuthenticated]
    )
    def add_rating(self, request, pk=None):
        """Add rating to the movie."""
        data = {
            'user': request.user.id,
            'movie_id': pk,
            'rating': request.data['rating'],
            'comment': request.data['comment']
            }
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()

            try:
                all_movie_ratings = Rating.objects.filter(movie_id=pk).values('rating')
                ratings = [rating['rating'] for rating in all_movie_ratings]
                average = round(sum(ratings) / len(ratings), 2)
                movie = Movie.objects.get(id=pk)
                movie.average_rating = average
                movie.save()
            except:
                return Response('Rating was saved, but average did not change.', status=400)

            return Response(serializer.data, status=200)
        
        return Response(serializer.errors, status=400)
    
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'add_rating':
            return serializers.ManageRatingSerializer

        return self.serializer_class


class RetrieveArtistView(generics.RetrieveAPIView):

    serializer_class = serializers.ArtistSerializer
    queryset = Artist.objects.all()

    def retrieve(self, request, pk):
        """Override retrieve method to retrieve artist with movies."""

        # retrieve artist
        instance = self.get_object()
        artist_serializer = self.get_serializer(instance)

        # retrieve directed movies
        directed = Movie.objects.filter(director=pk)
        directed_serializer = serializers.BasicMovieSerializer(directed, many=True)

        # retrieve starred movies
        starred = Movie.objects.filter(actors=pk)
        starred_serializer = serializers.BasicMovieSerializer(starred, many=True)

        data = artist_serializer.data
        data['Directed'] = directed_serializer.data
        data['Starred'] = starred_serializer.data

        return Response(data)
