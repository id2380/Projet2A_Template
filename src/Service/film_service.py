from src.Client.film_client import FilmClient
from src.dao.film_dao import FilmDAO


class FilmService:

    def recherche_films(self, title: str = None, page: int = 1,
                        language: str = "en-US",
                        primary_release_year: int = None, region: str = None,
                        year: int = None):
        films = None
        if title is None:
            films = FilmClient().recherche_films(page, language,
                                                 primary_release_year,
                                                 region,
                                                 year)
        else:
            films = FilmClient().recherche_films_titre(title, page, language,
                                                       primary_release_year,
                                                       region,
                                                       year)
        return films

    def creer_film(self, id_film: int):
        Film = FilmClient().recherche_film_id(id_film)
        print(Film)
        if Film is not None:
            boolean = FilmDAO().creer_film(Film)
            print("       Boolean     ")
            print(boolean)
            return boolean
        return False
