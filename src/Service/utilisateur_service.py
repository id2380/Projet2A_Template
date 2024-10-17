import hashlib

from src.business_object.utilisateur import Utilisateur
from src.dao.utilisateur_dao import UtilisateurDAO


class UtilisateurService:
    """Classe contenant les méthodes de service pour les Utilisateurs"""
    utilisateur_db: None

    def __init__(self, utilisateur_db: None):
        """Initialisation minimaliste de UtilisateurService"""
        self.utilisateur_db = utilisateur_db

    def hachage_mot_de_passe(self, mot_de_passe, sel=""):
        """Hachage du mot de passe avec option de sel"""
        mot_de_passe_bytes = mot_de_passe.encode("utf-8") + sel.encode("utf-8")
        hash_object = hashlib.sha256(mot_de_passe_bytes)
        return hash_object.hexdigest()

    def creation_compte(self, pseudo: str, mot_de_passe: str, adresse_email: str) -> Utilisateur:
        """Création d'un utilisateur à partir de ses attributs"""

        # Hashage du mot de passe avec le pseudo comme sel
        mot_de_passe_hash = self.hachage_mot_de_passe(mot_de_passe, pseudo)

        # Création de l'objet Utilisateur
        nouvel_utilisateur = Utilisateur(
            pseudo=pseudo,
            mot_de_passe=mot_de_passe_hash,
            adresse_email=adresse_email
        )

        # Sauvegarde de l'utilisateur en base de données
        utilisateur_dao = UtilisateurDAO()
        return nouvel_utilisateur if utilisateur_dao.creer(nouvel_utilisateur) else None
