import os
from unittest import mock

import pytest
from pydantic_core import ValidationError

from src.client.film_client import FilmClient


@mock.patch.dict(os.environ, {"WEBSERVICE_HOST": "https://api.themoviedb.org/3","WEBSERVICE_TOKEN":"Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0OTJhMmU0OTUyOTcwZDBmNWQ4ZTZiMjI2ZmFmZGMwNCIsIm5iZiI6MTcyNjgyMDY4My4zMDYxMjYsInN1YiI6IjY2ZWQyYzNiY2RkMTA4ZWQ5MzIyYWYzNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.2vVcbaxM_PX11RFgys6jhTskiwiV1t0fCChn8K0Hlxs"})
class TestFilmClient:
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

if __name__ == "__main__":
    import pytest

    pytest.main([__file__])