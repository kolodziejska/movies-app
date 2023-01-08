"""
URL mappings for the user API.
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from user import views


router = DefaultRouter()
router.register('ratings', views.RatingViewSet)

app_name='user'

urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('signup/', views.CreateUserView.as_view(), name='signup'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
