import pytest
from dotenv import load_dotenv

from src.client.genre_client import GenreClient


class TestGenreClient:
    """
    Une classe qui permet de tester les fonctionnalités de la classe
    genre_client.
    """

    load_dotenv(override=True)

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    """
    Teste la recherche des genres.
    """
    def test_recherche_genres_ok(self):
        # GIVEN
        genre_client = GenreClient()

        # WHEN AND THEN
        try:
            genre_client.recherche_genres()
            assert True
        except Exception:
            assert False

    """
    Teste la fonction genres.
    """
    def test_genres_ok(self):
        # GIVEN
        genre_client = GenreClient()

        # WHEN AND THEN
        try:
            genre_client.recherche_genres()
            liste_genres = genre_client.genres([16, 878])
            assert len(liste_genres) == 2
        except Exception:
            assert False


if __name__ == "__main__":
    pytest.main([__file__])
