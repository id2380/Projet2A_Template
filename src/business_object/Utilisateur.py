import hashlib
from datetime import datetime


class Utilisateur:
    def __init__(self, id_utilisateur, pseudo, email, mot_de_passe, date_creation=None):
        self.id_utilisateur = id
        self.pseudo = pseudo
        self.email = email
        self._mot_de_passe = self._hash_mot_de_passe(mot_de_passe)  # Stockage du hash du mot de passe
        self.date_creation = date_creation if date_creation else datetime.now()

    def __repr__(self):
        return f"<Utilisateur(id={self.id_utilisateur}, pseudo='{self.pseudo}', email='{self.email}')>"

    def _hash_mot_de_passe(self, mot_de_passe):
        """Hash le mot de passe avec SHA-256."""
        return hashlib.sha256(mot_de_passe.encode()).hexdigest()

    def verifier_mot_de_passe(self, mot_de_passe):
        """Vérifie si le mot de passe fourni correspond au hash stocké."""
        return self._mot_de_passe == hashlib.sha256(mot_de_passe.encode()).hexdigest()
    
    @property
    def mot_de_passe(self):
        """Rend le mot de passe inaccessible directement."""
        raise AttributeError("Le mot de passe ne peut pas être accédé directement.")

    @mot_de_passe.setter
    def mot_de_passe(self, nouveau_mot_de_passe):
        """Permet de définir un nouveau mot de passe, qui sera automatiquement hashé."""
        self._mot_de_passe = self._hash_mot_de_passe(nouveau_mot_de_passe)

