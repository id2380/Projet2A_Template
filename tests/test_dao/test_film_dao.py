from datetime import datetime

from src.business_object.film import Film
from src.dao.film_dao import FilmDAO


class TestFilmDao:
    def test_create_film_ok(self):
        # GIVEN
        film_dao = FilmDAO()
        film = Film(
            id_film=0,
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

<<<<<<< HEAD
=======
    def test_create_film_existant(self):
        # GIVEN
        film_dao = FilmDAO()
        film = Film(
            id_film=0,
            titre="Test",
            genre="Test",
            date_de_sortie=datetime(2024, 10, 21),
            langue_originale="Français",
            synopsis="Ceci est un test.",
        )
        # WHEN
        created = film_dao.creer_film(film)

        # THEN
        assert created == False

    
>>>>>>> 6572b1c79cc65b755f6994ee77b7ca9d55a03d63

if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
