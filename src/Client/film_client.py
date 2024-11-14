import os

import requests
from dotenv import load_dotenv

from src.client.genre_client import GenreClient
from src.Model.film import Film
from src.Model.film_complet import FilmComplet
from src.utils.date import parse_str
from src.utils.singleton import Singleton


class FilmClient(metaclass=Singleton):
    """
    Une classe qui permet de communiquer avec l'API Tmdb.
    """

    # -------------------------------------------------------------------------
    # Constructeur
    # -------------------------------------------------------------------------

    """
    Attributs
    ----------
    _HOST : str
        URL de l'API Tmdb.
    _headers : dict
        Les en-têtes HTTP.
    """
    def __init__(self) -> None:
        load_dotenv()
        self.__HOST = os.environ["WEBSERVICE_HOST"]
        self._headers = {"accept": "application/json",
                         "Authorization": os.environ["WEBSERVICE_TOKEN"]}

    # -------------------------------------------------------------------------
    # Méthodes
    # -------------------------------------------------------------------------

    def recherche_films(
        self,
        page: int = 1,
        language: str = "fr",
        primary_release_year: int = None,
    ):
        """
        Permet d'obtenir une liste de films actuellement populaires sur TMDb,
        avec leurs informations de base.

        Paramètres
        ----------
        page : int
            Le nombre de pages de films à charger dans l'API.
        language : str
            La langue utilisée dans l'API, par défaut c'est le français.
        primary_release_year : int
            L'année de première sortie du film.

        Retour
        ----------
        list[Film] : Liste de films populaires remplissant les
        caractéristiques en paramètres.

        Exception
        ----------
        valueError : erreur de communication avec l'API.
        """
        genre_client = GenreClient(language=language)
        genre_client.recherche_genres()
        url = f"{self.__HOST}/discover/movie"
        params = {
            "include_adult": False,
            "language": language,
            "include_video": False,
            "page": page,
            "sort_by": "popularity.desc",
            "primary_release_year": primary_release_year,
        }
        req = requests.get(url, headers=self._headers, params=params)
        films = []
        if req.status_code == 200:
            raw_films = req.json()["results"]
            for raw_film in raw_films:
                film = Film(
                    id_film=raw_film["id"],
                    titre=raw_film["title"],
                    genres=genre_client.genres(raw_film["genre_ids"]),
                    date_de_sortie=parse_str(raw_film["release_date"]),
                    langue_originale=raw_film["original_language"],
                    synopsis=raw_film["overview"],
                )
                if film:
                    films.append(film)
            return films
        raise ValueError("Problème de communication avec l'API Tmdb.")

    def recherche_films_titre(
        self,
        titre: str,
        page: int = 1,
        language: str = "fr",
        primary_release_year: int = None,
    ):
        """
        Permet d'obtenir une liste de films avec leurs informations de base les
        caractérisant et qui possèdent dans leur titre l'attribut titre.

        Paramètres
        ----------
        titre : str
            La chaîne de caractères qui doit être contenue dans le titre.
        page : int
            Le nombre de pages de films à charger dans l'API.
        language : str
            La langue utilisée dans l'API, par défaut c'est le français.
        primary_release_year : int
            L'année de première sortie du film.

        Retour
        ----------
        list[Film] : liste de films populaires remplissant les caractéristiques
        en paramètres.

        Exception
        ----------
        valueError : erreur de communication avec l'API.
        """
        genre_client = GenreClient(language=language)
        genre_client.recherche_genres()
        url = f"{self.__HOST}/search/movie"
        params = {
            "query": titre,
            "include_adult": False,
            "language": language,
            "include_video": False,
            "page": page,
            "sort_by": "popularity.desc",
            "primary_release_year": primary_release_year,
        }
        req = requests.get(url, headers=self._headers, params=params)
        films = []
        if req.status_code == 200:
            raw_films = req.json()["results"]
            for raw_film in raw_films:
                film = Film(
                    id_film=raw_film["id"],
                    titre=raw_film["title"],
                    genres=genre_client.genres(raw_film["genre_ids"]),
                    date_de_sortie=parse_str(raw_film["release_date"]),
                    langue_originale=raw_film["original_language"],
                    synopsis=raw_film["overview"],
                )

                if film:
                    films.append(film)
            return films
        raise ValueError("Problème de communication avec l'API Tmdb.")

    def recherche_film_id(
        self,
        id_film: int,
        language: str = "fr"
    ):
        """
        Permet d'obtenir les informations techniques d'un film ayant
        l'identifiant passé en paramètre.

        Paramètres
        ----------
        id_film : int
            L'identifiant du film recherché.
        language : str
            La langue utilisée dans l'API, par défaut c'est le français.

        Retour
        ----------
        FilmComplet : film recherché.

        Exception
        ----------
        valueError : erreur de communication avec l'API.
        valueError : identifiant du film non valide.
        """
        url = f"{self.__HOST}/movie/{id_film}"
        params = {"movie_id": id_film, "language": language}
        req = requests.get(url, headers=self._headers, params=params)
        if req.status_code == 200:
            proposition = req.json()
            film = FilmComplet(
                id_film=proposition["id"],
                titre=proposition["title"],
                genres=[genre["name"] for genre in proposition["genres"]],
                date_de_sortie=parse_str(proposition["release_date"]),
                langue_originale=proposition["original_language"],
                synopsis=proposition.get("overview", "Non spécifiée") ,
                budget=int(proposition.get("budget", 0) if proposition.get("budget") is not None else 0), 
                pays_origine=proposition.get("origin_country", ["Non spécifiée"])[0] ,
                societe_prod=proposition["production_companies"][0]["name"] if proposition["production_companies"] else "Non spécifiée",
                duree=proposition.get("runtime", "Non spécifiée"),
                revenue=int(proposition.get("revenue", 0) if proposition.get("revenue") is not None else 0)
            )
            return film
        elif req.status_code == 404:
            raise ValueError("L'identifiant n'est pas valide.")
        else:
            raise ValueError("Problème de communication avec l'API Tmdb.")

    def obtenir_films_similaires(
        self,
        id_film: int,
        language: str = "fr",
        page: int = 1
    ):
        """
        Permet d'obtenir une liste de films avec leurs informations de base les
        caractérisant et sont similaires avec le film dont l'identifiant est
        passé en paramètre.

        Paramètres
        ----------
        id_film : int
            L'identifiant du film.
        language : str
            La langue utilisée dans l'API, par défaut c'est le français.
        page : int
            Le nombre de pages de films à charger dans l'API.

        Retour
        ----------
        list[Film] : liste de films similaires au film passé en paramètre.

        Exception
        ----------
        valueError : erreur de communication avec l'API.
        valueError : identifiant du film non valide.
        """
        genre_client = GenreClient(language=language)
        genre_client.recherche_genres()
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
                    genres=genre_client.genres(raw_film["genre_ids"]),
                    date_de_sortie=parse_str(raw_film["release_date"]),
                    langue_originale=raw_film["original_language"],
                    synopsis=raw_film["overview"],
                )
                if film:
                    films.append(film)
            return films
        elif req.status_code == 404:
            raise ValueError("L'identifiant n'est pas valide.")
        else:
            raise ValueError("Problème de communication avec l'API Tmdb.")