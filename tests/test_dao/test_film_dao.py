from datetime import datetime

from src.dao.film_dao import FilmDAO
from src.Model.film import Film


class TestFilmDao:
    """
    Une classe qui permet de tester les fonctionnalités de la DAO pour
    lesfilms.
    """

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    """
    Teste l'ajout d'un film dans la base.
    """
    def test_creer_film_ok(self):
        # GIVEN
        film_dao = FilmDAO()
        film = Film(
            id_film=1,
            titre="Test",
            genres=["Test", "Test"],
            date_de_sortie=datetime(2024, 10, 21),
            langue_originale="Français",
            synopsis="Ceci est un test."
        )

        # WHEN AND THEN
        try:
            film_dao.creer_film(film)
            assert True
        except Exception:
            assert False

    """
    Teste la lecture d'un film dans la base.
    """
    def test_lire_film_existant(self):
        # GIVEN
        film_dao = FilmDAO()

        # WHEN AND THEN
        try:
            film = film_dao.lire_film(1)
            assert film is not None
        except Exception:
            assert False

    """
    Teste la lecture d'un film inexistant dans la base.
    """
    def test_lire_film_inexistant(self):
        # GIVEN
        film_dao = FilmDAO()

        # WHEN AND THEN
        try:
            film = film_dao.lire_film(2)
            assert film is None
        except Exception:
            assert False

    """
    Teste l'existence d'un film existant dans la base.
    """
    def test_existe_film_existant(self):
        # GIVEN
        film_dao = FilmDAO()

        # WHEN AND THEN
        try:
            boolean = film_dao.existe_film(1)
            assert boolean
        except Exception:
            assert False

    """
    Teste l'existence d'un film inexistant dans la base.
    """
    def test_existe_film_inexistant(self):
        # GIVEN
        film_dao = FilmDAO()

        # WHEN AND THEN
        try:
            boolean = film_dao.existe_film(2)
            assert not boolean
        except Exception:
            assert False

    """
    Teste la lecture de films dans la base.
    """
    def test_liste_films_ok(self):
        # GIVEN
        film_dao = FilmDAO()

        # WHEN AND THEN
        try:
            films = film_dao.liste_films()
            assert len(films) > 0
        except Exception:
            assert False

    """
    Teste la suppression d'un film dans la base.
    """
    def test_supprimer_film_ok(self):
        # GIVEN
        film_dao = FilmDAO()

        # WHEN AND THEN
        try:
            film_dao.supprimer_film(1)
            assert True
        except Exception:
            assert False


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
