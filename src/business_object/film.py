from datetime import datetime


class Film():

    """
    Une classe qui représente un film.
    """

    # -------------------------------------------------------------------------
    # Constructeur
    # -------------------------------------------------------------------------

    """
    Attributs
    ----------
    id_film : int
        Un identifiant unique du film.
    titre : string
        Le titre du film.
    genre : string
        Le genre du film.
    date_de_sortie : datetime
        Le jour, le mois et l'année de sortie du film.
    langue_originale : str
        La langue originale du film.
    synopsis : str
        Le résumé du film.
    """

    def __init__(self, id_film, titre, genre, date_de_sortie, langue_originale,
                 synopsis) -> None:

        # -----------------------------
        # Attributs
        # -----------------------------

        self._id_film: int = id_film
        self._titre: str = titre
        self._genre: str = genre
        self._date_de_sortie: datetime = date_de_sortie
        self._langue_originale: str = langue_originale
        self._synopsis: str = synopsis

    # -------------------------------------------------------------------------
    # Methodes
    # -------------------------------------------------------------------------

    def __str__(self):
        """
        Retourne un string représentant un objet Film.
        """
        return (f"Id_film: {self.id_film}\n"
                f"Titre: {self.titre}\n"
                f"Genre: {self.genre}\n"
                f"Date de sortie: {self.date_de_sortie}\n"
                f"Langue originale: {self.langue_originale}\n"
                f"Synopsis : {self.synopsis}")

    # -------------------------------------------------------------------------
    # Getters et Setters
    # -------------------------------------------------------------------------

    @property
    def id_film(self):
        return self._id_film

    @id_film.setter
    def id_film(self, value: int):
        self._id_film = value

    @property
    def titre(self):
        return self._titre

    @titre.setter
    def titre(self, value: str):
        self._titre = value

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value: str):
        self._genre = value

    @property
    def date_de_sortie(self):
        return self._date_de_sortie

    @date_de_sortie.setter
    def date_de_sortie(self, value: str):
        self._date_de_sortie = value

    @property
    def langue_originale(self):
        return self._langue_originale

    @langue_originale.setter
    def langue_originale(self, value: str):
        self._langue_originale = value

    @property
    def synopsis(self):
        return self._synopsis

    @synopsis.setter
    def synopsis(self, value: str):
        self._synopsis = value
