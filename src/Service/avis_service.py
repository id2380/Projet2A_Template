from src.dao.avis_dao import AvisDAO
from src.dao.utilisateur_dao import UtilisateurDAO
from src.Model.avis import Avis
from src.service.eclaireur_service import EclaireurService
from src.service.film_service import FilmService


class AvisService:
    """
    Classe contenant les méthodes de service pour les avis.
    """

    # -------------------------------------------------------------------------
    # Méthodes
    # -------------------------------------------------------------------------

    def ajouter_avis(self,
                     id_film: int,
                     id_utilisateur: int,
                     note: int,
                     commentaire: str):
        """
        Ajoute un nouvel avis via la DAO.

        Parameters
        ----------
        id_film : int
            L'identifiant du film pour lequel l'avis est créé.
        id_utilisateur : int
            L'id de l'utilisateur qui rédige l'avis.
        commentaire : str
            Le contenu de l'avis.
        note : int
            La note attribuée au film.

        Exception
        -------
        ValueError : si l'utilisateur n'existe pas.
        ValueError : si l'utilisateur a déjà partagé un avis pour ce film.
        ValueError : si problème de connexion avec la base.
        """
        film_service = FilmService()
        avis_dao = AvisDAO()
        if UtilisateurDAO().chercher_utilisateur_par_id(id_utilisateur) is None:
            raise ValueError("L'utilisateur n'existe pas. Vérifiez l'id.")
        if not film_service.existe_film(id_film):
            film_service.creer_film(id_film)
        if avis_dao.existe_avis(id_film, id_utilisateur):
            raise ValueError("L'utilisateur a déjà partagé un avis pour ce film")
        avis = Avis(id_film=id_film,
                    id_utilisateur=id_utilisateur,
                    note=note,
                    commentaire=commentaire)
        avis_dao.creer_avis(avis) 

    def obtenir_avis(self, id_film=None, id_utilisateur=None):
        """
        Recherche d'avis dans la base de données. Cette recherche peut être
        fait en ciblant les avis liés à un film, à un utilisateur ou les deux.

        Parameters
        ----------
        id_film : int
            L'id du film associé aux avis à rechercher.

        id_utilisateur : int
            L'id de l'utilisateur aux avis à rechercher.

        Return
        ----------
        avis : list[Avis]
            La liste des avis recherchés.

        Exception
        -------
        ValueError : erreur lors de la recherche d'avis dans la base.
        ValueError : si l'utilisateur n'existe pas.
        ValueError : si le film ne possède pas d'avis.
        ValueError : si l'utilisateur ne possède pas d'avis.
        ValueError : si la combinaison film, utilisateur ne possède pas d'avis.
        """
        film_service = FilmService()
        avis_dao = AvisDAO()
        if id_utilisateur is not None:
            if UtilisateurDAO().chercher_utilisateur_par_id(id_utilisateur) is None:
                raise ValueError("L'utilisateur n'existe pas. Vérifiez l'id.")
        if id_film is not None:
            if not film_service.existe_film(id_film):
                raise ValueError("Aucun avis n'a été partagé pour ce film.")
        avis = avis_dao.lire_avis(id_film=id_film,
                                  id_utilisateur=id_utilisateur) 
        if len(avis) == 0 and id_film is None:
            raise ValueError("Aucun avis n'a été partagé par cet utilisateur.")
        if len(avis) == 0 and id_film is not None:
            raise ValueError("Aucun avis ne correspond à vos critères.")
        return avis

    def modifier_avis(self, id_film: int,
                      id_utilisateur: int,
                      note: int,
                      commentaire: str):
        """
        Modification d'un avis dans la base de données.

        Parameters
        ----------
        id_film : int
            L'id du film pour l'avis.

        id_utilisateur : int
            L'id de l'utisateur pour l'avis.

        note : int
            La note de l'avis.

        commentaire : str
            Le commentaire de l'avis.

        Exception
        -------
        ValueError : erreur lors de la modification de l'avis dans la base.
        ValueError : si l'utilisateur n'existe pas.
        ValueError : si l'utilisateur n'a pas partagé d'avis pour ce film.
        """
        avis_dao = AvisDAO()
        if UtilisateurDAO().chercher_utilisateur_par_id(id_utilisateur) is None:
            raise ValueError("L'utilisateur n'existe pas. Vérifiez l'id.")
        if not avis_dao.existe_avis(id_film, id_utilisateur):
            raise ValueError("L'utilisateur n'a pas partagé d'avis pour ce film.")
        avis = Avis(id_film=id_film,
                    id_utilisateur=id_utilisateur,
                    note=note,
                    commentaire=commentaire)
        avis_dao.modifier_avis(avis)

    def supprimer_avis(self, id_film: int, id_utilisateur: int):
        """
        Supprime un avis via le DAO et supprime le film si c'était
        le dernier avis.

        Parameters
        ----------
        id_film : int
            L'identifiant du film auquel l'avis est associé.
        id_utilisateur : int
            L'id de l'utilisateur ayant posté l'avis.

        Exception
        -------
        ValueError : erreur lors de la suppression de l'avis dans la base.
        ValueError : si l'utilisateur n'existe pas.
        ValueError : si l'utilisateur n'a pas partagé d'avis pour ce film.
        """
        film_service = FilmService() 
        avis_dao = AvisDAO()
        if UtilisateurDAO().chercher_utilisateur_par_id(id_utilisateur) is None:
            raise ValueError("L'utilisateur n'existe pas. Vérifiez l'id.")
        if not avis_dao.existe_avis(id_film, id_utilisateur):
            raise ValueError("L'utilisateur n'a pas partagé d'avis pour ce film.")
        avis_dao.supprimer_avis(id_film, id_utilisateur)
        if len(avis_dao.lire_avis(id_film=id_film)) == 0:
            film_service.supprimer_film(id_film)

    def calculer_note_moyenne(self, id_film: int) -> float:
        """
        Calcule la note moyenne des avis pour un film spécifié.

        Parameters
        ----------
        id_film : int
            L'identifiant du film.

        Returns
        -------
        float
            La note moyenne des avis pour ce film.

        Exception
        -------
        ValueError : erreur lors de la lecture des avis dans la base.
        ValueError : si aucun avis n'est associé au film.
        """
        liste_avis = AvisDAO().lire_avis(id_film=id_film)
        if len(liste_avis) == 0:
            raise ValueError("Aucun avis pour ce film.")
        return sum(avis.note for avis in liste_avis) / len(liste_avis)

    def lire_avis_eclaireurs(self, id_film: int, id_utilisateur: int):
        """
        Recherche les avis sur un film des éclaireurs d'un utilisateur.

        Parameters
        ----------
        id_film : int
            L'id du film associé aux avis à rechercher.

        id_utilisateur : int
            L'id de l'utilisateur.

        Return
        ----------
        avis : list[Avis]
            La liste des avis recherchés.

        Exception
        -------
        ValueError : erreur lors de la recherche d'avis dans la base.
        ValueError : si l'utilisateur n'existe pas.
        ValueError : si aucun éclaireur n'a donné d'avis pour le film.
        """
        if UtilisateurDAO().chercher_utilisateur_par_id(id_utilisateur) is None:
            raise ValueError("L'utilisateur n'existe pas. Vérifiez l'id.")
        liste_id = [e.id_utilisateur for e in EclaireurService().liste_eclaireurs(id_utilisateur)]
        avis = AvisDAO(). lire_avis_eclaireurs(id_film, liste_id)
        if len(avis) == 0:
            raise ValueError("Aucun de vos éclaireurs n'a donné d'avis pour ce film.")
        return avis

    def calculer_note_moyenne_eclaireurs(self, id_film: int, id_utilisateur: int):
        """
        Calcule la note moyenne des avis des éclaireurs pour un film spécifié.

        Parameters
        ----------
        id_film : int
            L'identifiant du film.

        id_utilisateur : int
            L'identifiant de l'utilisateur.

        Returns
        -------
        float
            La note moyenne des avis des éclaireuspour ce film.

        Exception
        -------
        ValueError : erreur lors de la recherche d'avis dans la base.
        ValueError : si l'utilisateur n'existe pas.
        """
        if UtilisateurDAO().chercher_utilisateur_par_id(id_utilisateur) is None:
            raise ValueError("L'utilisateur n'existe pas. Vérifiez l'id.")
        liste_avis = self.lire_avis_eclaireurs(id_film, id_utilisateur)
        return sum(avis.note for avis in liste_avis) / len(liste_avis)

    def lire_avis_communs(self, id_utilisateur1: int, id_utilisateur2: int):
        """
        Recherche les avis associés à un même film pour deux utilisateurs.

        Parameters
        ----------
        id_utilisateur1 : int
            L'id du premier utilisateur.

        id_utilisateur2 : int
            L'id du second utilisateur.

        Return
        ----------
        avis : list[dict{"Avis1": Avis, "Avis2": Avis}]
            La liste des dictionnaires des avis associés au même film.

        Exception
        -------
        ValueError : erreur lors de la recherche d'avis dans la base.
        ValueError : si l'utilisateur1 n'existe pas.
        ValueError : si l'utilisateur2 n'existe pas.
        ValueError : si aucun avis sur le même film.
        """
        utilisateur_dao = UtilisateurDAO()
        if utilisateur_dao.chercher_utilisateur_par_id(id_utilisateur1) is None:
            raise ValueError("L'utilisateur1 n'existe pas. Vérifiez l'id.")
        if utilisateur_dao.chercher_utilisateur_par_id(id_utilisateur2) is None:
            raise ValueError("L'utilisateur2 n'existe pas. Vérifiez l'id.")
        avis = AvisDAO().lire_avis_communs(id_utilisateur1, id_utilisateur2)
        if len(avis) == 0:
            raise ValueError("Aucun film en commun entre les utilisateurs.")
        return avis
