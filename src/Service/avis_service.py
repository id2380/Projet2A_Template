from src.business_object.avis import Avis
from src.dao.avis_dao import AvisDAO
from src.service.film_service import FilmService
from typing import Optional

class AvisService:
    def __init__(self):
        # Initialisation de l'objet AvisDAO
        self.avis_dao = AvisDAO()

    def ajouter_avis(self, id_film: int, utilisateur: str, commentaire: str,note: int,) -> Optional[Avis]:
        """
        Ajoute un nouvel avis via le DAO.

        Parameters
        ----------
        id_film : int
            L'identifiant du film pour lequel l'avis est créé.
        utilisateur_pseudo : str
            Le pseudo de l'utilisateur qui rédige l'avis.
        commentaire : str
            Le contenu de l'avis.
        note : int
            La note attribuée au film.

        Returns
        -------
        Avis or None
            L'avis créé, ou None si l'ajout a échoué.
        """
        # Création d'un nouvel objet Avis
        film_service = FilmService() 
        nouvel_avis = Avis(id_avis=None, id_film=id_film, utilisateur=utilisateur,  commentaire=commentaire,note=note)
        if not film_service.existe_film(nouvel_avis.id_film):
                        print(
                            f"Le film avec l'ID '{nouvel_avis.id_film}' n'a pas été trouvé dans la base. Création en cours via l'API TMDB..."
                        )
                        film_created = film_service.creer_film(nouvel_avis.id_film)
                        if not film_created :
                            print(f"Impossible de créer le film avec l'ID '{nouvel_avis.id_film}' via l'API TMDB.")
                            return False
                        print(f"Film avec l'ID '{nouvel_avis.id_film}' créé avec succès.")
        # Utilisation de l'AvisDAO pour créer l'avis dans la base de données
        if self.avis_dao.creer_avis(nouvel_avis):
            return nouvel_avis
        return f"Erreur : Un avis existe déjà pour ce film par cet utilisateur."

    def obtenir_avis_par_film(self, id_film: int) -> list:
        """
        Obtient tous les avis pour un film donné.

        Parameters
        ----------
        id_film : int
            L'identifiant du film.

        Returns
        -------
        list
            Liste des avis pour ce film.
        """
        return self.avis_dao.lire_avis(id_film=id_film)

    def obtenir_avis_par_utilisateur_pseudo(self, utilisateur_pseudo: str) -> list:
        """
        Obtient tous les avis rédigés par un utilisateur donné.

        Parameters
        ----------
        utilisateur_pseudo : str
            Le pseudo de l'utilisateur dont on souhaite récupérer les avis.

        Returns
        -------
        list
            Liste des avis rédigés par cet utilisateur.
        """
        return self.avis_dao.lire_avis(utilisateur=utilisateur_pseudo)
    def obtenir_avis_par_utilisateur_identifiant(self, id_utilisateur:int)->list : 
        """
        Obtient tous les avis rédigés par l'identifiant d'un utilisateur donné.

        Parameters
        ----------
        id_utilisateur : int
            l'identifiant de l'utilisateur dont on souhaite récupérer les avis.

        Returns
        -------
        list
            Liste des avis rédigés par cet utilisateur.
        """
        return self.avis_dao.lire_avis(id_utilisateur=id_utilisateur)
    def modifier_avis(self, id_film: int, utilisateur: str, commentaire: str, note: int) -> bool:
        """
        Modifie un avis existant via le DAO.

        Parameters
        ----------
        id_film : int
            L'identifiant du film auquel l'avis est associé.
        utilisateur_pseudo : str
            Le pseudo de l'utilisateur ayant posté l'avis.
        commentaire : str
            Le nouveau commentaire de l'avis.
        note : int
            La nouvelle note attribuée au film.

        Returns
        -------
        bool
            True si la modification a réussi, False sinon.
        """
        film_service = FilmService()
        avis = Avis(id_avis=None, id_film=id_film, utilisateur=utilisateur, commentaire=commentaire, note=note)
        if not film_service.existe_film(avis.id_film):
                        print(f"Le film avec l'ID '{avis.id_film}' n'existe pas dans la base de données.")
                        return False
        # Utilisation du DAO pour modifier l'avis
        return self.avis_dao.modifier_avis(avis)
    
    def supprimer_avis(self, id_film: int, utilisateur: str) -> bool:
        """
        Supprime un avis via le DAO et supprime le film si c'était
        le dernier avis.

        Parameters
        ----------
        id_film : int
            L'identifiant du film auquel l'avis est associé.
        utilisateur_pseudo : str
            Le pseudo de l'utilisateur ayant posté l'avis.

        Returns
        -------
        bool
            True si la suppression a réussi, False sinon.
        """
        return self.avis_dao.supprimer_avis(id_film=id_film, utilisateur=utilisateur)

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
        """
        avis_list = self.avis_dao.lire_avis(id_film=id_film)

        # Si aucun avis n'est trouvé, on retourne 0.0
        if not avis_list or avis_list == "Aucun avis trouvé.":
            return 0.0

        # Calcul de la somme des notes
        total_notes = sum(avis.note for avis in avis_list)

        # Retour de la moyenne des notes
        return total_notes / len(avis_list)

