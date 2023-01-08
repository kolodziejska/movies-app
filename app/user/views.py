"""
Views for the user API.
"""
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import viewsets, generics, authentication, permissions

from user.serializers import AuthTokenSerializer, UserSerializer
from movie.serializers import ManageRatingSerializer
from core.models import Rating


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create new token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class RatingViewSet(viewsets.ModelViewSet):
    """View for viewing and editing user's ratings."""
    serializer_class = ManageRatingSerializer
    http_method_names = ['get', 'patch']
    queryset = Rating.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(user_id=self.request.user.id)
