import csv
import os
from django.utils.text import slugify

from core.models import Movie, Artist, Genre


def run():
    """
    Import example data from csv file.
    Dataset from: https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows
    """

    file_path = os.path.join('example_data', 'imdb_top_1000.csv')

    Movie.objects.all().delete()

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:

            genre_models = list()

            genres = row['Genre'].strip('"').split(', ')
            for genre in genres:
                g, _ = Genre.objects.get_or_create(genre=genre)
                genre_models.append(g)
            
            data = row['Director'].split(maxsplit=1)
            name = data[0]
            surname = data[-1]

            director, _ = Artist.objects.get_or_create(
                first_name=name, 
                last_name=surname, 
                slug=slugify(f'{name} {surname}'))
            
            year = row['Released_Year'] if row['Released_Year'].isnumeric() else '0'

            movie = Movie(
                title=row['Series_Title'],
                year=year,
                overview=row['Overview']
            )

            movie.save()
            movie.director.add(director)

            for actor in ['Star1', 'Star2', 'Star3', 'Star4']:
                data = row[actor].split(maxsplit=1)
                name = data[0]
                surname = data[-1]
                star, _ = Artist.objects.get_or_create(
                    first_name=name, 
                    last_name=surname, 
                    slug=slugify(f'{name} {surname}'))
                movie.actors.add(star)

            for genre in genre_models:
                movie.genre.add(genre)
            
            movie.slug = f'{slugify(movie.title[:45])}-{movie.id}'
            movie.save()

