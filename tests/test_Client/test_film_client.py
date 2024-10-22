import pytest

from src.client.film_client import FilmClient


class TestFilmClient:
    import dotenv
    dotenv.load_dotenv(override=True)

    # methode recherche_films
    def test_recherche_films_ok(self):
        # GIVEN
        film_client = FilmClient()
        # WHEN
        films = film_client.recherche_films()
        # THEN
        assert films is not None

    def test_recherche_films_error(self):
        # GIVEN
        film_client = FilmClient()
        # WHEN
        films = film_client.recherche_films(page="test", language=3)
        # THEN
        assert films is None

    # methode recherche_films_titre
    def test_recherche_films_titre_ok(self):
        # GIVEN
        film_client = FilmClient()
        # WHEN
        films = film_client.recherche_films_titre("robot")
        # THEN
        assert films is not None

    def test_recherche_films_titre_error(self):
        # GIVEN
        film_client = FilmClient()
        # WHEN
        films = film_client.recherche_films_titre("robot", page="test")
        # THEN
        assert films is None

    # methode obtenir_films_similaires
    def test_obtenir_films_similaires_ok(self, id_film=1184918):
        # GIVEN
        film_client = FilmClient()
        # WHEN
        films = film_client.obtenir_films_similaires(id_film)
        # THEN
        assert films is not None

    def test_obtenir_films_similaires_error(self, id_film=0):
        # GIVEN
        film_client = FilmClient()
        # WHEN
        films = film_client.obtenir_films_similaires(id_film)
        # THEN
        assert films is None


if __name__ == "__main__":
    pytest.main([__file__])
