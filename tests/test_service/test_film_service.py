from unittest.mock import MagicMock

from src.client.film_client import FilmClient
from src.Service.film_service import FilmService


class TestFilmService:
    import dotenv
    dotenv.load_dotenv(override=True)

    def test_recherche_films_titre(self):
        # GIVEN
        film_service = FilmService()
        FilmClient().recherche_films_titre = MagicMock(return_value=[])
        # WHEN
        films = film_service.recherche_films("robot")
        # THEN
        assert films is not None

    def test_recherche_films(self):
        # GIVEN
        film_service = FilmService()
        FilmClient().recherche_films = MagicMock(return_value=[])
        # WHEN
        films = film_service.recherche_films()
        # THEN
        assert films is not None

    def test_recherche_films_erreur(self):
        # GIVEN
        film_service = FilmService()
        FilmClient().recherche_films_titre = MagicMock(return_value=None)
        # WHEN
        films = film_service.recherche_films("robot", page="test")
        # THEN
        assert films is None


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
