from unittest import mock
from unittest.mock import MagicMock

from src.client.film_client import FilmClient
from src.service.film_service import FilmService
from src.service.avis_service import AvisService
from src.dao.avis_dao import AvisDAO


class TestFilmService:
    """
    Une classe qui permet de tester les fonctionnalités des services pour
    les films.
    """

    import dotenv
    dotenv.load_dotenv(override=True)

    """
    Teste la recherche de films par titre
    """
    def test_recherche_films_titre(self):
        # GIVEN
        film_service = FilmService()
        FilmClient().recherche_films_titre = MagicMock(return_value=["film"])

        # WHEN AND THEN
        try:
            films = film_service.recherche_films("robot")
            assert len(films) > 0
        except Exception:
            assert False

    """
    Teste la recherche de films quand aucun film ne correspond
    au critère.
    """
    def test_recherche_films_titre_erreur(self):
        # GIVEN
        film_service = FilmService()
        FilmClient().recherche_films_titre = MagicMock(return_value=[])

        # WHEN AND THEN
        try:
            film_service.recherche_films("ccekce,cekc e")
            assert False
        except Exception:
            assert True

    """
    Teste la recherche de films.
    """
    def test_recherche_films(self):
        # GIVEN
        film_service = FilmService()
        FilmClient().recherche_films = MagicMock(return_value=["film"])

        # WHEN AND THEN
        try:
            films = film_service.recherche_films()
            assert len(films) > 0
        except Exception:
            assert False

    """
    Teste la recherche de films similaires.
    """
    def test_recherche_films_similaires_ok(self):
        # GIVEN
        film_service = FilmService()
        FilmClient().obtenir_films_similaires = MagicMock(return_value=["film"])

        # WHEN AND THEN
        try:
            films = film_service. recherche_films_similaires(id_film=1184918)
            assert len(films) > 0
        except Exception:
            assert False

    """
    Teste la recherche de films similaires avec aucun film similaire.
    """
    def test_recherche_films_similaires_aucun(self):
        # GIVEN
        film_service = FilmService()
        FilmClient().obtenir_films_similaires = MagicMock(return_value=[])

        # WHEN AND THEN
        try:
            film_service. recherche_films_similaires(id_film=1184918)
            assert False
        except Exception as e:
            assert str(e) == "Aucun film n'est similaire au film."
    

    

    """
    @mock.patch("src.dao.film_dao.FilmDAO.creer_film")
    @mock.patch("src.Client.film_client.FilmClient.recherche_film_id")
    def test_creer_film_ok(self, mock_recherche_film_id, mock_creer_film):
        # GIVEN
        mock_recherche_film_id.return_value = []
        mock_creer_film.return_value = True
        film_service = FilmService()
        # WHEN
        boolean = film_service.creer_film(1184918)
        # THEN
        assert boolean

    @mock.patch("src.Client.film_client.FilmClient.recherche_film_id")
    def test_creer_film_inexistant(self, mock_recherche_film_id):
        # GIVEN
        mock_recherche_film_id.return_value = None
        film_service = FilmService()
        # WHEN
        boolean = film_service.creer_film(1184918)
        # THEN
        assert boolean is False

    @mock.patch("src.dao.film_dao.FilmDAO.creer_film")
    @mock.patch("src.Client.film_client.FilmClient.recherche_film_id")
    def test_creer_film_erreur(self, mock_recherche_film_id, mock_creer_film):
        # GIVEN
        mock_recherche_film_id.return_value = []
        mock_creer_film.return_value = False
        film_service = FilmService()
        # WHEN
        boolean = film_service.creer_film(1184918)
        # THEN
        assert boolean is False
    """


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
