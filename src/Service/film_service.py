from src.client.film_client import FilmClient


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
