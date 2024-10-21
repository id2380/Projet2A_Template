import os

import requests

from src.business_object.film import Film
from src.utils.singleton import Singleton


class FilmClient(metaclass=Singleton):
    def __init__(self) -> None:
        self.__HOST = os.environ["WEBSERVICE_HOST"]
        self._headers = {"accept": "application/json",
                         "Authorization": os.environ["WEBSERVICE_TOKEN"]}

    def search_movies(self, page: int = 1, language: str = "en-US"):
        url = f"{self.__HOST}/discover/movie"
        params = {"include_adult": False,
                  "language": language,
                  "include_video": False,
                  "page": page,
                  "sort_by": "popularity.desc"}
        req = requests.get(url, headers=self._headers, params=params)
        # GENRE A COMPLETER !!!!!!
        films = []
        if req.status_code == 200:
            raw_films = req.json()["results"]
            for raw_film in raw_films:
                film = Film(id_film=raw_film["id"],
                            titre=raw_film["title"],
                            genre="",
                            date_de_sortie=raw_film["release_date"],
                            langue_originale=raw_film["original_language"],
                            synopsis=raw_film["overview"])

                if film:
                    films.append(film)
            return films
        else:
            return None

    def getSimilarMovies(self, movieId: int, language: str = "en-US",
                         page: int = 1):
        url = f"{self.__HOST}/movie/{movieId}/similar"
        params = {"language": language,
                  "page": page}
        req = requests.get(url, headers=self._headers, params=params)

        films = []
        print(req.status_code)
        if req.status_code == 200:
            raw_films = req.json()["results"]
            for raw_film in raw_films:
                film = Film(id_film=raw_film["id"],
                            titre=raw_film["title"],
                            genre="",
                            date_de_sortie=raw_film["release_date"],
                            langue_originale=raw_film["original_language"],
                            synopsis=raw_film["overview"])

                if film:
                    films.append(film)
            return films
        else:
            return None


# Pour tester, à supprimer par la suite
if __name__ == "__main__":
    # Pour charger les variables d'environnement contenues dans le fichier .env
    import dotenv
    dotenv.load_dotenv(override=True)

    filmClient = FilmClient()

    print(filmClient.search_movies())

    print(filmClient.getSimilarMovies(1184918))
