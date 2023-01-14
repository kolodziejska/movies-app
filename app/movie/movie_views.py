"""
Views for movie/movies API.
"""

from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from django.utils.text import slugify

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
    lookup_field = "slug"

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
    
    def retrieve(self, request, slug):
        """Override retrieve method to retrieve movie with ratings."""

        # retrieve movie
        instance = self.get_object()
        movie_serializer = self.get_serializer(instance)

        # retrieve ratings
        ratings = Rating.objects.filter(movie_id=instance.id)
        ratings_serializer = serializers.RatingSerializer(ratings, many=True)

        data = movie_serializer.data
        data['Ratings'] = ratings_serializer.data

        return Response(data)

    def create(self, request):
        """Override create method to add genres and artists and autogenerate slug."""
        data = request.data.copy()
        genres = data.pop('genre', None)
        directors = data.pop('director', None)
        actors = data.pop('actors', None)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # add genres
        if genres:
            for genre in genres:
                genre_model, _ = Genre.objects.get_or_create(genre=genre['genre'])
                instance.genre.add(genre_model)
        
        # add directors
        if directors:
            for director in directors:
                first_name, last_name = director["first_name"], director["last_name"]
                director_model, created = Artist.objects.get_or_create(
                    first_name=first_name,
                    last_name=last_name
                )
                if created:
                    director_model.slug = slugify(
                        f"{first_name} {last_name} {director_model.id}")
                    director_model.save()
                instance.director.add(director_model)

        
        # add actors
        if actors:
            for actor in actors:
                first_name, last_name = actor["first_name"], actor["last_name"]
                actor_model, created = Artist.objects.get_or_create(
                    first_name=first_name,
                    last_name=last_name
                )
                if created:
                    actor_model.slug = slugify(
                        f"{first_name} {last_name} {actor_model.id}")
                    actor_model.save()
                instance.actors.add(actor_model)

        # generate slug
        if not instance.slug:
            slug_title = f"{instance.title} {instance.id}"
            instance.slug=slugify(slug_title)
        instance.save()
        return Response(serializer.data, status=200)
    
    @action(
        methods=['post'],
        detail=True,
        url_path='add_rating',
        authentication_classes = [TokenAuthentication],
        permission_classes = [IsAuthenticated]
    )
    def add_rating(self, request, slug=None):
        """Add rating to the movie."""

        movie_id = slug.split("-")[-1]
        data = {
            'user': request.user.id,
            'movie_id': movie_id,
            'rating': request.data['rating'],
            'comment': request.data['comment']
            }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        try:
            all_movie_ratings = Rating.objects.filter(movie_id=movie_id).values('rating')
            ratings = [rating['rating'] for rating in all_movie_ratings]
            average = round(sum(ratings) / len(ratings), 2)
            movie = Movie.objects.get(id=movie_id)
            movie.average_rating = average
            movie.save()
        except:
            return Response('Rating was saved, but average did not change.', status=400)

        return Response(serializer.data, status=200)
    
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'add_rating':
            return serializers.ManageRatingSerializer
        elif self.action == 'create':
            return serializers.CreateMovieSerializer

        return self.serializer_class
