from django.db.models import QuerySet
from django.db import transaction

from db.models import Movie


def get_movies(
        title: str = None,
        genres_ids: list = None,
        actors_ids: list = None
) -> QuerySet[Movie]:
    movies = Movie.objects.all()

    if title is not None:
        movies = movies.filter(title__icontains=title)

    if genres_ids is not None:
        movies = movies.filter(genres__id__in=genres_ids).distinct()

    if actors_ids is not None:
        movies = movies.filter(actors__id__in=actors_ids).distinct()

    return movies


@transaction.atomic
def create_movie(
        movie_title: str,
        movie_description: str,
        actors: list = None,
        genres: list = None,
        actors_ids: list = None,
        genres_ids: list = None,
) -> Movie:
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description
    )

    if actors_ids:
        movie.actors.set(actors_ids)
    elif actors:
        movie.actors.set(actors)

    if genres_ids:
        movie.genres.set(genres_ids)
    elif genres:
        movie.genres.set(genres)

    return movie
