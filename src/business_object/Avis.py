from src.business_object.film import Film
from src.business_object.utilisateur import Utilisateur


class Avis:
    def __init__(self, id, film, utilisateur, note, commentaire):
        self.id_avis = id
        self.film = film
        self.utilisateur = utilisateur
        self.note = note
        self.commentaire = commentaire

    def __repr__(self):
        return f"<Avis(id={self.id_avis}, film={self.film.titre}, utilisateur={self.utilisateur.pseudo}, note={self.note})>"
