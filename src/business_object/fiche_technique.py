from datetime import datetime


class FicheTechnique:
    """ Classe représentant une fiche technique d'un film.

    Attributes
    ----------
    _id_film : int or None
        L'identifiant unique du film associé.
    _nom_film : str
        Le nom du film.
    _budget : int
        Le budget du film
    _genres : list(str)
        Les genres associés aux films
    _pays_origine : str
        Le pays d'ou vient le film
    _langue_originale : str
        La langue originale du film
    _date_sortie : datetime
        La date à laquelle le film est parru
    """

    def __init__(self, id_film: int, nom_film: str, budget: int,
                 genres: list(str), pays_origine: str,
                 langue_originale: str, date_sortie: datetime):
        """
        Initialise une nouvelle fiche technique avec les informations fournies.
        """
        self._id_film = id_film
        self._nom_film = nom_film
        self._budget = budget
        self._genres = genres
        self._pays_origine = pays_origine
        self._langue_originale = langue_originale
        self._date_sortie = date_sortie

    @property
    def id_film(self) -> int:
        return self._id_film

    @id_film.setter
    def id_film(self, value: int):
        self._id_film = value

    @property
    def nom_film(self) -> str:
        return self._nom_film

    @nom_film.setter
    def nom_film(self, value: str):
        self._nom_film = value

    @property
    def budget(self) -> int:
        return self._budget

    @budget.setter
    def budget(self, value: int):
        self._budget = value

    @property
    def genres(self) -> list(str):
        return self._genres

    @genres.setter
    def genres(self, value: list(str)):
        self._genres = value

    @property
    def pays_origine(self) -> str:
        return self._pays_origine

    @pays_origine.setter
    def pays_origines(self, value: str):
        self._pays_origine = value

    @property
    def langue_originale(self) -> str:
        return self._langue_originale

    @langue_originale.setter
    def langue_originale(self, value: str):
        self._langue_originale = value

    @property
    def date_sortie(self) -> datetime:
        return self._date_sortie

    @date_sortie.setter
    def date_sortie(self, value: datetime):
        self._date_sortie = value
