from datetime import datetime

from src.business_object.film import Film
from src.dao.film_dao import FilmDAO


class TestFilmDao:
    def test_create_film_ok(self):
        # GIVEN
        film_dao = FilmDAO()
        film = Film(
            id_film=3,
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
            id_film=3,
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

<<<<<<< HEAD
=======
    
>>>>>>> 54c42a43633d7f86931c7f624c7444d73699a58f

if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
