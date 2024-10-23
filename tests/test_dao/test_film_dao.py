from datetime import datetime

from src.business_object.film import Film
from src.dao.film_dao import FilmDAO
from src.data.db_connection import DBConnection


class TestFilmDao:
    def test_creer_film_ok(self):
        # GIVEN
        film_dao = FilmDAO()
        film = Film(
            id_film=500,
            titre="Test",
            genre="Test",
            date_de_sortie=datetime(2024, 10, 21),
            langue_originale="Français",
            synopsis="Ceci est un test.",
            fiche_technique=None
        )
        # WHEN
        boolean = film_dao.creer_film(film)
        # THEN
        assert boolean

    def test_creer_film_existant(self):
        # GIVEN
        film_dao = FilmDAO()
        film = Film(
            id_film=300,
            titre="Test",
            genre="Test",
            date_de_sortie=datetime(2024, 10, 21),
            langue_originale="Français",
            synopsis="Ceci est un test.",
            fiche_technique=None
        )
        # WHEN
        boolean = film_dao.creer_film(film)
        # THEN
        assert boolean is False

    def test_lire_film_existant(self):
        # GIVEN
        film_dao = FilmDAO()
        # WHEN
        film = film_dao.lire_film(300)
        # THEN
        assert film is not None

    def test_lire_film_inexistant(self):
        # GIVEN
        film_dao = FilmDAO()
        # WHEN
        film = film_dao.lire_film(1000)
        # THEN
        assert film is None

    def test_supprimer_film_existant(self):
        # GIVEN
        film_dao = FilmDAO()
        # WHEN
        boolean = film_dao.supprimer_film(300)
        # THEN
        assert boolean is True

    def test_supprimer_film_inexistant(self):
        # GIVEN
        film_dao = FilmDAO()
        # WHEN
        boolean = film_dao.supprimer_film(300)
        # THEN
        assert boolean is False


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
