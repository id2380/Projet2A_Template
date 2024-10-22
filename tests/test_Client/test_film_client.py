import os
from unittest import mock

import pytest
from pydantic_core import ValidationError

from src.client.film_client import FilmClient


class TestFilmClient:
    import dotenv
    dotenv.load_dotenv(override=True)
    # methode search_movies
    def test_search_movies_ok(self):
        # GIVEN
        film_client = FilmClient()

        # WHEN
        films = film_client.search_movies()

        # THEN
        assert films is not None

    def test_search_movies_properties_ok(self):
        # GIVEN
        film_client = FilmClient()

        # WHEN
        films = film_client.search_movies(page=3)

        # THEN
        assert films is not None

    def test_search_movies_error(self):
        # GIVEN
        film_client = FilmClient()

        # WHEN
        films = film_client.search_movies(page="test", language=3)

        # THEN
        assert films is None

    # methode search_movies
    def test_search_movies_title_ok(self):
        # GIVEN
        film_client = FilmClient()

        # WHEN
        films = film_client.search_movies_title("robot")

        # THEN
        assert films is not None

    def test_search_movies_title_error(self):
        # GIVEN
        film_client = FilmClient()

        # WHEN
        films = film_client.search_movies_title("robot", page="test")

        # THEN
        assert films is None

    # methode getSimilarMovies

    def test_getSimilarMovies_ok(self, movieId=1184918):
        # GIVEN
        film_client = FilmClient()

        # WHEN
        films = film_client.getSimilarMovies(movieId)

        # THEN
        assert films is not None

    def test_getSimilarMovies_error(self, movieId=0):
        # GIVEN
        film_client = FilmClient()

        # WHEN
        films = film_client.getSimilarMovies(movieId)

        # THEN
        assert films is None


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
