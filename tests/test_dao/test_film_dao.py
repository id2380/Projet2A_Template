from datetime import datetime

from src.business_object.film import Film
from src.dao.film_dao import FilmDAO


class TestFilmDao:
    def test_create_film_ok(self):
        # GIVEN
        film_dao = FilmDAO()
        film = Film(
            id_film=9,
            titre="Test",
            genre="Test",
            date_de_sortie=datetime(2024, 10, 21),
            langue_originale="Français",
            synopsis="Ceci est un test.",
        )
        # WHEN
        created = film_dao.creer_film(film)

        # THEN
        assert created

    def test_create_film_existant(self):
        # GIVEN
        film_dao = FilmDAO()
        film = Film(
            id_film=9,
            titre="Test",
            genre="Test",
            date_de_sortie=datetime(2024, 10, 21),
            langue_originale="Français",
            synopsis="Ceci est un test.",
        )
        # WHEN
        created = film_dao.creer_film(film)

        # THEN
        assert created is False

    def test_read_film_existant(self, movieId=9):
        # GIVEN
        film_dao = FilmDAO()
        # WHEN
        read = film_dao.read_film(movieId)
        # THEN
        assert read is not None

    def test_read_film_inexistant(self, movieId=10):
        # GIVEN
        film_dao = FilmDAO()
        # WHEN
        read = film_dao.read_film(movieId)
        # THEN
        assert read is None

    def test_delete_film_existant(self, movieId=9):
        # GIVEN
        film_dao = FilmDAO()
        # WHEN
        delete = film_dao.delete_film(movieId)
        # THEN
        assert delete is True

    def test_delete_film_inexistant(self, movieId=10):
        # GIVEN
        film_dao = FilmDAO()
        # WHEN
        delete = film_dao.delete_film(movieId)
        # THEN
        assert delete is False


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
