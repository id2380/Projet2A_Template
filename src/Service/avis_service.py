from src.business_object.avis import Avis
from src.business_object.film import Film
from src.dao.avis_dao import AvisDAO
from src.Model.utilisateur import Utilisateur


class AvisService:
    def __init__(self, avis_dao: AvisDAO):
        self.avis_dao = avis_dao

    def ajouter_avis(self, id_film: int, utilisateur: Utilisateur, commentaire: str, note: int) -> Avis:
        """
        Ajoute un nouvel avis via le DAO.
        
        Parameters
        ----------
        id_film : int
            L'identifiant du film pour lequel l'avis est créé.
        utilisateur : Utilisateur
            L'utilisateur qui rédige l'avis.
        commentaire : str
            Le contenu de l'avis.
        note : int
            La note attribuée au film.

        Returns
        -------
        Avis or None
            L'avis créé, ou None si l'ajout a échoué.
        """
        nouvel_avis = Avis(id_avis=None, id_film=id_film, utilisateur=utilisateur, note=note, commentaire=commentaire)
        return nouvel_avis if self.avis_dao.creer_avis(nouvel_avis) else None

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
        return self.avis_dao.lire_avis(id_film=id_film)  # Utiliser l'ID du film

    def obtenir_avis_par_utilisateur(self, utilisateur: Utilisateur) -> list:
        """
        Obtient tous les avis rédigés par un utilisateur donné.
        
        Parameters
        ----------
        utilisateur : Utilisateur
            L'utilisateur dont on souhaite récupérer les avis.

        Returns
        -------
        list
            Liste des avis rédigés par cet utilisateur.
        """
        return self.avis_dao.lire_avis(utilisateur=utilisateur.pseudo)  # Utiliser le pseudo de l'utilisateur

    def modifier_avis(self, id_avis: int, utilisateur: str, id_film: int, commentaire: str, note: int) -> bool:
        """
        Modifie un avis existant via le DAO.
        
        Parameters
        ----------
        id_avis : int
            L'identifiant de l'avis à modifier.
        utilisateur : str
            Le pseudo de l'utilisateur ayant posté l'avis.
        id_film : int
            L'identifiant du film auquel l'avis est associé.
        commentaire : str
            Le nouveau commentaire de l'avis.
        note : int
            La nouvelle note attribuée au film.

        Returns
        -------
        bool
            True si la modification a réussi, False sinon.
        """
        avis = Avis(id_avis=id_avis, id_film=id_film, utilisateur=utilisateur, commentaire=commentaire, note=note)
        return self.avis_dao.modifier_avis(avis)

    def supprimer_avis(self, avis_id: int, utilisateur: str, id_film: int) -> bool:
        """
        Supprime un avis via le DAO et supprime le film si c'était le dernier avis.

        Parameters
        ----------
        avis_id : int
            L'identifiant de l'avis à supprimer.
        utilisateur : str
            Le pseudo de l'utilisateur ayant posté l'avis.
        id_film : int
            L'identifiant du film auquel l'avis est associé.

        Returns
        -------
        bool
            True si la suppression a réussi, False sinon.
        """
        return self.avis_dao.supprimer_avis(avis_id=avis_id, utilisateur=utilisateur, id_film=id_film)

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
        avis_list = self.avis_dao.lire_avis(id_film=id_film)  # Utiliser l'ID du film
        if not avis_list or avis_list == "Aucun avis trouvé.":
            return 0.0  # Retourne 0 si aucun avis n'est disponible
        total_notes = sum(avis.note for avis in avis_list)
        return total_notes / len(avis_list)
