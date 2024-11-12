from src.client.film_client import FilmClient
from src.dao.film_dao import FilmDAO


class FilmService:
    def recherche_films(
        self,
        title: str = None,
        page: int = 1,
        language: str = "fr",
        primary_release_year: int = None,
        region: str = None,
        year: int = None,
    ):
        if title is None:
            films = FilmClient().recherche_films(page,
                                                    language,
                                                    primary_release_year,
                                                    region,
                                                    year)
        else:
            films = FilmClient().recherche_films_titre(title,
                                                        page,
                                                        language,
                                                        primary_release_year,
                                                        region,
                                                        year)
        if len(films) == 0:
            raise ValueError("Aucun film ne correspond à vos critères.")
        return films

    def creer_film(self, id_film: int):
        Film = FilmClient().recherche_film_id(id_film)
        if Film is not None:
            boolean = FilmDAO().creer_film(Film)
            return boolean
        return False

    def recherche_films_similaires(self, id_film: int, language: str = "en-US", page: int = 1):
        films = FilmClient().obtenir_films_similaires(id_film, language, page)
        return films

    def obtenir_film_complet(self, id_film: int):
        film_complet = FilmClient().recherche_film_id(id_film)
        return film_complet


if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv(override=True)

    film_service = FilmService()
    print(film_service.creer_film(1184918))
