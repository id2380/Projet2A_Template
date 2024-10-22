import os

from src.business_object.film import Film
from src.client.film_client import FilmClient


class FilmService:

    def recherche_films(self, title: str = None, page: int = 1, language: str = "en-US", primary_release_year: int = None, region: str = None, year: int = None):
        films = None
        if title is None:
            films = FilmClient().search_movies(page, language, primary_release_year, region, year)
        else:
            films = FilmClient().search_movies_title(title, page, language, primary_release_year, region, year)
        return films
