from datetime import datetime


class Film():
    """ Film """

    def __init__(self, id_film, titre, genre, date_de_sortie, langue_originale,
                 synopsis) -> None:
        self._id_film: int = id
        self._titre: str = titre
        self._genre: str = genre
        self._date_de_sortie: datetime = date_de_sortie
        self._langue_originale: str = langue_originale
        self._synopsis: str = synopsis

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
