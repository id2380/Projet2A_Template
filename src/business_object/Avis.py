from src.business_object.utilisateur import Utilisateur


class Avis:
    def __init__(self, id_avis, id_film, utilisateur, note, commentaire):
        self.id_avis = id_avis
        self.id_film = id_film
        self.utilisateur = utilisateur
        self.note = note
        self.commentaire = commentaire

    def __repr__(self):
        return f"<Avis(id_avis={self.id_avis}, id_film={self.id_film}, utilisateur={self.utilisateur}, note={self.note})>"
