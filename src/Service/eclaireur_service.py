from src.dao.eclaireur_dao import EclaireurDAO
from src.dao.utilisateur_dao import UtilisateurDAO


class EclaireurService:
    def ajouter_eclaireur_id(self, id_utilisateur: int, id_eclaireur: int):
        eclaireur_dao = EclaireurDAO()
        if UtilisateurDAO().chercher_utilisateur_par_id(id_eclaireur) is None:
            raise ValueError("L'éclaireur n'existe pas. Vérifiez l'id.")
        if eclaireur_dao.est_eclaireur(id_utilisateur, id_eclaireur):
            raise ValueError("Vous êtes déjà abonnés à cet utilisateur.")
        eclaireur_dao.ajouter_eclaireur(id_utilisateur, id_eclaireur)

    def ajouter_eclaireur_pseudo(self, id_utilisateur: int,
                                 pseudo_eclaireur: str):
        eclaireur = UtilisateurDAO().chercher_utilisateur_par_pseudo(pseudo_eclaireur)
        eclaireur_dao = EclaireurDAO()
        if eclaireur is None:
            raise ValueError("L'éclaireur n'existe pas. Vérifiez le pseudo.")
        if eclaireur_dao.est_eclaireur(id_utilisateur,
                                       eclaireur.id_utilisateur):
            raise ValueError("Vous êtes déjà abonnés à cet utilisateur.")
        eclaireur_dao.ajouter_eclaireur(id_utilisateur,
                                        eclaireur.id_utilisateur)

    def est_eclaireur_id(self, id_utilisateur: int, id_eclaireur: int):
        if UtilisateurDAO().chercher_utilisateur_par_id(id_eclaireur) is None:
            raise ValueError("L'éclaireur n'existe pas. Vérifiez l'id.")
        return EclaireurDAO().est_eclaireur(id_utilisateur, id_eclaireur)

    def est_eclaireur_pseudo(self, id_utilisateur: int,
                             pseudo_eclaireur: str):
        eclaireur = UtilisateurDAO().chercher_utilisateur_par_pseudo(pseudo_eclaireur)
        if eclaireur is None:
            raise ValueError("L'éclaireur n'existe pas. Vérifiez le pseudo.")
        return EclaireurDAO().est_eclaireur(id_utilisateur,
                                            eclaireur.id_utilisateur)

    def supprimer_eclaireur_id(self, id_utilisateur: int, id_eclaireur: int):
        eclaireur_dao = EclaireurDAO()
        if UtilisateurDAO().chercher_utilisateur_par_id(id_eclaireur) is None:
            raise ValueError("L'éclaireur n'existe pas. Vérifiez l'id.")
        if eclaireur_dao.est_eclaireur(id_utilisateur, id_eclaireur) is False:
            raise ValueError(f"{id_eclaireur} ne fait pas partie de vos éclaireurs.")         
        eclaireur_dao.supprimer_eclaireur(id_utilisateur, id_eclaireur)

    def supprimer_eclaireur_pseudo(self, id_utilisateur: int, pseudo_eclaireur: str):
        eclaireur_dao = EclaireurDAO()
        eclaireur = UtilisateurDAO().chercher_utilisateur_par_pseudo(pseudo_eclaireur)
        if eclaireur is None:
            raise ValueError("L'éclaireur n'existe pas. Vérifiez le pseudo.")
        if eclaireur_dao.est_eclaireur(id_utilisateur, eclaireur.id_utilisateur) is False:
            raise ValueError(f"{pseudo_eclaireur} ne fait pas partie de vos éclaireurs.")         
        eclaireur_dao.supprimer_eclaireur(id_utilisateur, eclaireur.id_utilisateur)

    def liste_eclaireurs(self, id_utilisateur: int):
        return EclaireurDAO().liste_eclaireurs(id_utilisateur)