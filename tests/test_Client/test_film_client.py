import pytest
from dotenv import load_dotenv

from src.client.film_client import FilmClient


class TestFilmClient:
    """
    Une classe qui permet de tester les fonctionnalités de la classe
    film_client.
    """

    load_dotenv(override=True)

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    """
    Teste la recherche de films.
    """
    def test_recherche_films_ok(self):
        # GIVEN
        film_client = FilmClient()

        # WHEN AND THEN
        try:
            films = film_client.recherche_films()
            assert films is not None
        except Exception:
            assert False

    """
    Teste la recherche de films par titre.
    """
    def test_recherche_films_titre_ok(self):
        # GIVEN
        film_client = FilmClient()

        # WHEN AND THEN
        try:
            films = film_client.recherche_films_titre("robot")
            assert films is not None
        except Exception:
            assert False

    """
    Teste la recherche d'un film par son id avec un id valide.
    """
    def test_recherche_film_id_ok(self):
        # GIVEN
        film_client = FilmClient()

        # WHEN AND THEN
        try:
            film = film_client.recherche_film_id(id_film=1184918)
            assert film is not None
        except Exception:
            assert False

    """
    Teste la recherche d'un film par son id avec un id invalide.
    """
    def test_recherche_film_id_invalide(self):
        # GIVEN
        film_client = FilmClient()

        # WHEN AND THEN
        try:
            film_client.recherche_film_id(id_film=0)
            assert False
        except Exception as e:
            assert str(e) == "L'identifiant n'est pas valide."

    """
    Teste la recherche de films similaires à un film par son id avec un id
    valide.
    """
    def test_obtenir_films_similaires_ok(self):
        # GIVEN
        film_client = FilmClient()

        # WHEN AND THEN
        try:
            films = film_client.obtenir_films_similaires(id_film=1184918)
            assert films is not None
        except Exception:
            assert False

    """
    Teste la recherche de films similaires à un film par son id avec un id
    invalide.
    """
    def test_obtenir_films_similaires_invalide(self):
        # GIVEN
        film_client = FilmClient()

        # WHEN AND THEN
        try:
            film_client.obtenir_films_similaires(id_film=0)
            assert False
        except Exception as e:
            assert str(e) == "L'identifiant n'est pas valide."


if __name__ == "__main__":
    pytest.main([__file__])
