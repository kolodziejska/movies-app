"""
URL mappings for movie API.
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from movie import movie_views, artist_views


router = DefaultRouter()
router.register('movies', movie_views.MovieViewSet)

app_name = 'movie'

urlpatterns = [
    path('', include(router.urls)),
    path('artist/<str:slug>/', artist_views.RetrieveArtistView.as_view(), name='artist'),
    path('create-artist/', artist_views.CreateArtistView.as_view(), name='create-artist')
]
