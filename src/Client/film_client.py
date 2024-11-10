import os
from datetime import datetime

import requests

from src.Model.film import Film
from src.Model.film_complet import FilmComplet
from src.utils.singleton import Singleton


class FilmClient(metaclass=Singleton):
    def __init__(self) -> None:
        self.__HOST = os.environ["WEBSERVICE_HOST"]
        self._headers = {"accept": "application/json", "Authorization": os.environ["WEBSERVICE_TOKEN"]}

    def recherche_films(
        self,
        page: int = 1,
        language: str = "en-US",
        primary_release_year: int = None,
        region: str = None,
        year: int = None,
    ):
        url = f"{self.__HOST}/discover/movie"
        params = {
            "include_adult": False,
            "language": language,
            "include_video": False,
            "page": page,
            "sort_by": "popularity.desc",
            "primary_release_year": primary_release_year,
            "region": region,
            "year": year,
        }
        req = requests.get(url, headers=self._headers, params=params)
        # GENRE A COMPLETER !!!!!!
        films = []
        if req.status_code == 200:
            raw_films = req.json()["results"]
            for raw_film in raw_films:
                film = Film(
                    id_film=raw_film["id"],
                    titre=raw_film["title"],
                    genre="",
                    date_de_sortie=self.parse_str(raw_film["release_date"]),
                    langue_originale=raw_film["original_language"],
                    synopsis=raw_film["overview"],
                )
                if film:
                    films.append(film)
            return films
        else:
            return None

    def recherche_films_titre(
        self,
        titre: str,
        page: int = 1,
        language: str = "en-US",
        primary_release_year: int = None,
        region: str = None,
        year: int = None,
    ):
        url = f"{self.__HOST}/search/movie"
        params = {
            "query": titre,
            "include_adult": False,
            "language": language,
            "include_video": False,
            "page": page,
            "sort_by": "popularity.desc",
            "primary_release_year": primary_release_year,
            "region": region,
            "year": year,
        }
        req = requests.get(url, headers=self._headers, params=params)
        # GENRE A COMPLETER !!!!!!
        films = []
        if req.status_code == 200:
            raw_films = req.json()["results"]
            for raw_film in raw_films:
                film = Film(
                    id_film=raw_film["id"],
                    titre=raw_film["title"],
                    genre="",
                    date_de_sortie=self.parse_str(raw_film["release_date"]),
                    langue_originale=raw_film["original_language"],
                    synopsis=raw_film["overview"],
                )

                if film:
                    films.append(film)
            return films
        else:
            return None

    def recherche_film_id(self, id_film: int, language: str = "en-US"):
        url = f"{self.__HOST}/movie/{id_film}"
        params = {"movie_id": id_film, "language": language}
        req = requests.get(url, headers=self._headers, params=params)
        # GENRE A COMPLETER !!!!!!
        film = None
        if req.status_code == 200:
            proposition = req.json()
            film = FilmComplet(
                id_film=proposition["id"],
                titre=proposition["title"],
                genre="",
                date_de_sortie=self.parse_str(proposition["release_date"]),
                langue_originale=proposition["original_language"],
                synopsis=proposition["overview"],
                budget=proposition["budget"],
                pays_origine=proposition["origin_country"][0],
                societe_prod=proposition["production_companies"][0]["name"],
                duree=proposition["runtime"],
                revenue=proposition["revenue"],
            )
        return film

    def obtenir_films_similaires(self, id_film: int, language: str = "en-US", page: int = 1):
        url = f"{self.__HOST}/movie/{id_film}/similar"
        params = {"language": language, "page": page}
        req = requests.get(url, headers=self._headers, params=params)

        films = []
        if req.status_code == 200:
            raw_films = req.json()["results"]
            for raw_film in raw_films:
                film = Film(
                    id_film=raw_film["id"],
                    titre=raw_film["title"],
                    genre="",
                    date_de_sortie=self.parse_str(raw_film["release_date"]),
                    langue_originale=raw_film["original_language"],
                    synopsis=raw_film["overview"],
                )

                if film:
                    films.append(film)
            return films
        else:
            return None

    def parse_str(self, date: str):
        if date != "":
            return datetime.strptime(date, "%Y-%m-%d")
        return None


# Pour tester, à supprimer par la suite
if __name__ == "__main__":
    # Pour charger les variables d'environnement contenues dans le fichier .env
    import dotenv

    dotenv.load_dotenv(override=True)

    film_client = FilmClient()

    film = film_client.recherche_film_id(1184918)

    print(film.date_de_sortie)
