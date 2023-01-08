"""
URL mappings for movie API.
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from movie import views


router = DefaultRouter()
router.register('movies', views.MovieViewSet)

app_name = 'movie'

urlpatterns = [
    path('', include(router.urls)),
    path('artist/<int:pk>/', views.RetrieveArtistView.as_view(), name='artist')
]
