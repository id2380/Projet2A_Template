from src.dao.eclaireur_dao import EclaireurDAO
from src.dao.utilisateur_dao import UtilisateurDAO
from src.Model.api_utilisateur import APIUtilisateur


class EclaireurService:
    """
    Classe contenant les méthodes de service pour les éclaireurs.
    """

    # -------------------------------------------------------------------------
    # Méthodes
    # -------------------------------------------------------------------------

    """
    Permet à un utilisateur de s'abonner à un éclaireur à partir de son
    identifiant uniquement si l'identifiant est bien associé à un utilisateur
    et si l'abonnement n'était pas déjà effectif.

    Paramètres
    ----------
    id_utilisateur : int
        L'identifiant unique de l'utilisateur qui souhaite s'abonner.
    id_eclaireur : int
        L'identifiant unique de l'utilisateur auquel on souhaite s'abonner.

    Exception
    ----------
    ValueError : si une erreur survient lors de l'ajout de l'abonnement.
    ValueError : si l'éclaireur n'existe pas.
    ValueError : si déjà abonné à l'éclaireur.
    """
    def ajouter_eclaireur_id(self, id_utilisateur: int, id_eclaireur: int):
        eclaireur_dao = EclaireurDAO()
        if UtilisateurDAO().chercher_utilisateur_par_id(id_eclaireur) is None:
            raise ValueError("L'éclaireur n'existe pas. Vérifiez l'id.")
        if eclaireur_dao.est_eclaireur(id_utilisateur, id_eclaireur):
            raise ValueError("Vous êtes déjà abonnés à cet utilisateur.")
        eclaireur_dao.ajouter_eclaireur(id_utilisateur, id_eclaireur)

    """
    Permet à un utilisateur de s'abonner à un éclaireur à partir de son
    pseudo uniquement si celui-ci est bien associé à un utilisateur et
    si l'abonnement n'était pas déjà effectif.

    Paramètres
    ----------
    id_utilisateur : int
        L'identifiant unique de l'utilisateur qui souhaite s'abonner.
    pseudo_eclaireur : pseudo
        Le pseudo unique de l'utilisateur auquel on souhaite s'abonner.

    Exception
    ----------
    ValueError : si une erreur survient lors de l'ajout de l'abonnement.
    ValueError : si l'éclaireur n'existe pas.
    ValueError : si déjà abonné à l'éclaireur.
    """
    def ajouter_eclaireur_pseudo(self, id_utilisateur: int, pseudo_eclaireur: str):
        eclaireur = UtilisateurDAO().chercher_utilisateur_par_pseudo(pseudo_eclaireur)
        eclaireur_dao = EclaireurDAO()
        if eclaireur is None:
            raise ValueError("L'éclaireur n'existe pas. Vérifiez le pseudo.")
        if eclaireur_dao.est_eclaireur(id_utilisateur, eclaireur.id_utilisateur):
            raise ValueError("Vous êtes déjà abonnés à cet utilisateur.")
        eclaireur_dao.ajouter_eclaireur(id_utilisateur, eclaireur.id_utilisateur)

    """
    Vérifie si un utilisateur est abonné à un éclaireur à partir de son
    identifiant uniquement si l'identifiant est bien associé à un utilisateur.

    Paramètres
    ----------
    id_utilisateur : int
        L'identifiant unique de l'utilisateur pour lequel l'abonnement est
        vérifié.
    id_eclaireur : int
        L'identifiant unique de l'utilisateur qui est supposé être suivi par
        l'utilisateur.

    Retour
    ----------
    bool : True si l'utilisateur est abonné à l'éclaireur, False sinon.

    Exception
    ----------
    ValueError : si une erreur survient lors de la vérification.
    ValueError : si l'éclaireur n'existe pas.
    """
    def est_eclaireur_id(self, id_utilisateur: int, id_eclaireur: int):
        if UtilisateurDAO().chercher_utilisateur_par_id(id_eclaireur) is None:
            raise ValueError("L'éclaireur n'existe pas. Vérifiez l'id.")
        return EclaireurDAO().est_eclaireur(id_utilisateur, id_eclaireur)

    """
    Vérifie si un utilisateur est abonné à un éclaireur à partir de son
    pseudo uniquement si le pseudo est bien associé à un utilisateur.

    Paramètres
    ----------
    id_utilisateur : int
        L'identifiant unique de l'utilisateur pour lequel l'abonnement est
        vérifié.

    pseudo_eclaireur : str
        Le pseudo unique de l'utilisateur qui est supposé être suivi par
        l'utilisateur.

    Retour
    ----------
    bool : True si l'utilisateur est abonné à l'éclaireur, False sinon.

    Exception
    ----------
    ValueError : si une erreur survient lors de la vérification.
    ValueError : si l'éclaireur n'existe pas.
    """
    def est_eclaireur_pseudo(self, id_utilisateur: int, pseudo_eclaireur: str):
        eclaireur = UtilisateurDAO().chercher_utilisateur_par_pseudo(pseudo_eclaireur)
        if eclaireur is None:
            raise ValueError("L'éclaireur n'existe pas. Vérifiez le pseudo.")
        return EclaireurDAO().est_eclaireur(id_utilisateur, eclaireur.id_utilisateur)

    """
    Supprime l'abonnement d'un utilisateur à un éclaireur à partir de son
    identifiant uniquement si l'identifiant est bien associé à un utilisateur
    et si l'utilisateut est bien abonné à cet éclaireur.

    Paramètres
    ----------
    id_utilisateur : int
        L'identifiant unique de l'utilisateur pour lequel on souhaite
        supprimer l'abonnement.
    id_eclaireur : int
        L'identifiant unique de l'éclaireur dont on souhaite supprimer
        l'abonnement.

    Exception
    ----------
    ValueError : si une erreur survient lors de la suppression.
    ValueError : si l'éclaireur n'existe pas.
    ValueError : si pas encore abonné à l'éclaireur.
    """
    def supprimer_eclaireur_id(self, id_utilisateur: int, id_eclaireur: int):
        eclaireur_dao = EclaireurDAO()
        if UtilisateurDAO().chercher_utilisateur_par_id(id_eclaireur) is None:
            raise ValueError("L'éclaireur n'existe pas. Vérifiez l'id.")
        if eclaireur_dao.est_eclaireur(id_utilisateur, id_eclaireur) is False:
            raise ValueError(f"{id_eclaireur} ne fait pas partie de vos éclaireurs.")
        eclaireur_dao.supprimer_eclaireur(id_utilisateur, id_eclaireur)

    """
    Supprime l'abonnement d'un utilisateur à un éclaireur à partir de son
    pseudo uniquement si le pseudo est bien associé à un utilisateur
    et si l'utilisateut est bien abonné à cet éclaireur.

    Paramètres
    ----------
    id_utilisateur : int
        L'identifiant unique de l'utilisateur pour lequel on souhaite
        supprimer l'abonnement.
    pseudo_eclaireur : int
        Le pseudo unique de l'éclaireur dont on souhaite supprimer
        l'abonnement.

    Exception
    ----------
    ValueError : si une erreur survient lors de la suppression.
    ValueError : si l'éclaireur n'existe pas.
    ValueError : si pas encore abonné à l'éclaireur.
    """
    def supprimer_eclaireur_pseudo(self, id_utilisateur: int, pseudo_eclaireur: str):
        eclaireur_dao = EclaireurDAO()
        eclaireur = UtilisateurDAO().chercher_utilisateur_par_pseudo(pseudo_eclaireur)
        if eclaireur is None:
            raise ValueError("L'éclaireur n'existe pas. Vérifiez le pseudo.")
        if eclaireur_dao.est_eclaireur(id_utilisateur, eclaireur.id_utilisateur) is False:
            raise ValueError(f"{pseudo_eclaireur} ne fait pas partie de vos éclaireurs.")
        eclaireur_dao.supprimer_eclaireur(id_utilisateur, eclaireur.id_utilisateur)

    """
    Renvoie la liste des éclaireurs auxquels un utilisateur est abonné.

    Paramètres
    ----------
    id_utilisateur : int
        L'identifiant unique de l'utilisateur pour lequel on souhaite obtenir
        la liste de ses éclaireurs.

    Retour
    ----------
    list : liste des éclaireurs associés à l'utilisateur.

    Exception
    ----------
    ValueError : si une erreur survient lors de récupération des id.
    """
    def liste_eclaireurs(self, id_utilisateur: int):
        liste = []
        for id in EclaireurDAO().liste_eclaireurs(id_utilisateur):
            utilisateur = UtilisateurDAO().chercher_utilisateur_par_id(id)
            liste += [APIUtilisateur(id_utilisateur=utilisateur.id_utilisateur, pseudo=utilisateur.pseudo)]
        return liste
