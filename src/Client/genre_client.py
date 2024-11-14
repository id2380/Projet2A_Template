import os

import requests
from dotenv import load_dotenv

from src.utils.singleton import Singleton


class GenreClient(metaclass=Singleton):
    """
    Une classe qui permet de communiquer avec l'API Tmdb pour manipuler les
    genres de films.
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
    _genres : dict
        L'ensemble des identifiants de genre et le nom associé.
    _language : str
        La langue utilisée dans l'API, par défaut le français.
    """
    def __init__(self, language: str = "fr") -> None:
        load_dotenv()
        self.__HOST = os.environ["WEBSERVICE_HOST"]
        self._headers = {"accept": "application/json",
                         "Authorization": os.environ["WEBSERVICE_TOKEN"]}
        self._genres = {}
        self._language = language

    # -------------------------------------------------------------------------
    # Méthodes
    # -------------------------------------------------------------------------

    def recherche_genres(self):
        """
        Permet de rechercher dans l'API Tmdb les différents genre de films.

        Exception
        ----------
        valueError : erreur de communication avec l'API.
        """
        url = f"{self.__HOST}/genre/movie/list"
        params = {
            "language": self._language
        }
        req = requests.get(url, headers=self._headers, params=params)
        if req.status_code == 200:
            raw_genres = req.json()["genres"]
            for raw_genre in raw_genres:
                self._genres[raw_genre["id"]] = raw_genre["name"]
        else:
            raise ValueError("Problème de communication avec l'API Tmdb.")

    def genres(self, liste_id):
        """
        Permet de transformer une liste d'identifiants de genres en une liste
        de genre.

        Paramètres
        ----------
        liste_id : liste[int]
            La liste des identifiants de genres.

        Retour
        ----------
        list[string] : La lite des genres.
        """
        return [self._genres[id] for id in liste_id if id in self._genres]
