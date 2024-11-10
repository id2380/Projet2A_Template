from src.dao.utilisateur_dao import UtilisateurDAO
from src.Model.utilisateur import Utilisateur
from src.service.mot_de_passe_service import creer_sel, hacher_mot_de_passe, verifier_robustesse_mot_de_passe


class UtilisateurService:
    """Classe contenant les méthodes de service pour les Utilisateurs."""

    def __init__(self, utilisateur_dao: UtilisateurDAO):
        """
        Initialise le service utilisateur avec un DAO.

        Parameters
        ----------
        utilisateur_dao : UtilisateurDAO
            Le DAO utilisé pour accéder et gérer les utilisateurs dans la base de données.
        """
        self.utilisateur_dao = utilisateur_dao

    def creation_compte(self, pseudo: str, adresse_email: str, mot_de_passe: str) -> Utilisateur:
        """
        Crée un nouveau compte utilisateur.

        Parameters
        ----------
        pseudo : str
            Le pseudo choisi par l'utilisateur.
        adresse_email : str
            L'adresse email de l'utilisateur.
        mot_de_passe : str
            Le mot de passe de l'utilisateur (sera vérifié et haché).

        Returns
        -------
        Utilisateur ou None
            L'utilisateur créé avec succès, ou None si la création échoue.
        """
        # Vérification de la robustesse du mot de passe
        verifier_robustesse_mot_de_passe(mot_de_passe)

        # Création d'un sel unique pour l'utilisateur
        sel = creer_sel()

        # Hachage du mot de passe avec le sel
        mot_de_passe_hash = hacher_mot_de_passe(mot_de_passe, sel)

        # Création de l'objet Utilisateur
        nouvel_utilisateur = Utilisateur(
            pseudo=pseudo, adresse_email=adresse_email, mot_de_passe=mot_de_passe_hash, sel=sel
        )

        # Sauvegarde de l'utilisateur en base de données
        return nouvel_utilisateur if self.utilisateur_dao.creer(nouvel_utilisateur) else None

    def modifier_pseudo(self, id_utilisateur: int, nouveau_pseudo: str) -> Utilisateur | None:
        """
        Modifie le pseudo d'un utilisateur existant.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant unique de l'utilisateur à modifier.
        nouveau_pseudo : str
            Le nouveau pseudo à assigner.

        Returns
        -------
        Utilisateur ou None
            L'utilisateur mis à jour, ou None si la modification échoue.
        """
        modification_reussie = self.utilisateur_dao.modifier_pseudo(id_utilisateur, nouveau_pseudo)
        return self.utilisateur_dao.chercher_utilisateur_par_id(id_utilisateur) if modification_reussie else None

    def modifier_adresse_email(self, id_utilisateur: int, nouvelle_adresse_email: str) -> Utilisateur | None:
        """
        Modifie l'adresse email d'un utilisateur existant.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant unique de l'utilisateur à modifier.
        nouvelle_adresse_email : str
            La nouvelle adresse email à assigner.

        Returns
        -------
        Utilisateur ou None
            L'utilisateur mis à jour, ou None si la modification échoue.
        """
        modification_reussie = self.utilisateur_dao.modifier_adresse_email(id_utilisateur, nouvelle_adresse_email)
        return self.utilisateur_dao.chercher_utilisateur_par_id(id_utilisateur) if modification_reussie else None

    def modifier_mot_de_passe(self, id_utilisateur: int, nouveau_mot_de_passe: str) -> Utilisateur | None:
        """
        Modifie le mot de passe d'un utilisateur.

        Note
        ----
        Le mot de passe est vérifié pour sa robustesse et haché avec le sel existant.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant unique de l'utilisateur à modifier.
        nouveau_mot_de_passe : str
            Le nouveau mot de passe en clair (sera haché dans cette méthode).

        Returns
        -------
        Utilisateur ou None
            L'utilisateur mis à jour, ou None si la modification échoue.
        """
        # Vérification de la robustesse du nouveau mot de passe
        verifier_robustesse_mot_de_passe(nouveau_mot_de_passe)

        # Récupérer l'utilisateur pour obtenir le sel actuel
        utilisateur = self.utilisateur_dao.chercher_utilisateur_par_id(id_utilisateur)
        if utilisateur is None:
            print(f"Utilisateur avec ID {id_utilisateur} introuvable.")
            return None

        # Hacher le nouveau mot de passe avec le sel existant
        mot_de_passe_hash = hacher_mot_de_passe(nouveau_mot_de_passe, utilisateur.sel)

        # Mettre à jour le mot de passe dans la base
        modification_reussie = self.utilisateur_dao.modifier_mot_de_passe(id_utilisateur, mot_de_passe_hash)
        return self.utilisateur_dao.chercher_utilisateur_par_id(id_utilisateur) if modification_reussie else None

    def supprimer_compte(self, id_utilisateur: int) -> bool:
        """
        Supprime le compte d'un utilisateur de la base de données.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant unique de l'utilisateur à supprimer.

        Returns
        -------
        bool
            True si la suppression a réussi, False sinon.
        """
        return self.utilisateur_dao.supprimer_utilisateur(id_utilisateur)
