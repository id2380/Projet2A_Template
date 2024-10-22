from unittest import mock
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

    @mock.patch('src.dao.film_dao.FilmDAO.creer_film')
    @mock.patch('src.client.film_client.FilmClient.recherche_film_id')
    def test_creer_film_ok(self, mock_recherche_film_id, mock_creer_film):
        # GIVEN
        mock_recherche_film_id.return_value = []
        mock_creer_film.return_value = True
        film_service = FilmService()
        # WHEN
        boolean = film_service.creer_film(1184918)
        # THEN
        assert boolean

    @mock.patch('src.client.film_client.FilmClient.recherche_film_id')
    def test_creer_film_inexistant(self, mock_recherche_film_id):
        # GIVEN
        mock_recherche_film_id.return_value = None
        film_service = FilmService()
        # WHEN
        boolean = film_service.creer_film(1184918)
        # THEN
        assert boolean is False

    @mock.patch('src.dao.film_dao.FilmDAO.creer_film')
    @mock.patch('src.client.film_client.FilmClient.recherche_film_id')
    def test_creer_film_erreur(self, mock_recherche_film_id, mock_creer_film):
        # GIVEN
        mock_recherche_film_id.return_value = []
        mock_creer_film.return_value = False
        film_service = FilmService()
        # WHEN
        boolean = film_service.creer_film(1184918)
        # THEN
        assert boolean is False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
