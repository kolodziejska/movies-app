"""
Database models.
"""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MaxValueValidator, MinValueValidator


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create. save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'


class Artist(models.Model):
    """Artist object. (Artist can be either actor or director or both.)"""
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    slug = models.SlugField(null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Movie(models.Model):
    """The movie object."""
    title = models.CharField(max_length=45)
    year = models.IntegerField()
    genre = models.ManyToManyField('Genre')
    director = models.ManyToManyField('Artist')
    actors = models.ManyToManyField('Artist', related_name='+')
    overview = models.TextField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    average_rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    """Rating object."""
    movie_id = models.ForeignKey('Movie', on_delete=models.CASCADE)
    rating = models.IntegerField(default=3, validators=[
        MaxValueValidator(10), MinValueValidator(1)
    ])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.rating} by {self.user}'


class Genre(models.Model):
    """Genre object."""
    genre = models.CharField(max_length=45)

    def __str__(self):
        return self.genre
