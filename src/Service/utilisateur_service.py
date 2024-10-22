from src.Model.utilisateur import Utilisateur
from src.dao.utilisateur_dao import UtilisateurDAO
from src.Service.mot_de_passe_service import verifier_robustesse_mot_de_passe, creer_sel, hacher_mot_de_passe


class UtilisateurService:
    """Classe contenant les méthodes de service pour les Utilisateurs."""

    def __init__(self, utilisateur_dao: UtilisateurDAO):
        """Initialisation avec le DAO utilisateur."""
        self.utilisateur_dao = utilisateur_dao

    def creation_compte(self, pseudo: str, adresse_email: str, mot_de_passe: str) -> Utilisateur:
        """Création d'un utilisateur à partir de ses attributs, avec gestion du mot de passe."""

        # Vérification de la robustesse du mot de passe
        verifier_robustesse_mot_de_passe(mot_de_passe)

        # Création d'un sel unique pour l'utilisateur
        sel = creer_sel()

        # Hachage du mot de passe avec le sel
        mot_de_passe_hash = hacher_mot_de_passe(mot_de_passe, sel)

        # Création de l'objet Utilisateur
        nouvel_utilisateur = Utilisateur(
            pseudo=pseudo,
            adresse_email=adresse_email,
            mot_de_passe=mot_de_passe_hash,
            sel=sel
        )

        # Sauvegarde de l'utilisateur en base de données
        return nouvel_utilisateur if self.utilisateur_dao.creer(nouvel_utilisateur) else None



