from src.business_object.avis import Avis
from src.dao.avis_dao import AvisDAO


class AvisService:
    def __init__(self, avis_dao: AvisDAO):
        self.avis_dao = avis_dao

<<<<<<< HEAD
    def ajouter_avis(self, id_film: int, utilisateur: str, commentaire: str, note: int) -> Avis:
=======
    def ajouter_avis(self, id_film: int, utilisateur_pseudo: str,
                     commentaire: str, note: int) -> Avis:
>>>>>>> 4fb9a755b2c0e51597614ce73f7a3fa064b7eaf3
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
        return self.avis_dao.lire_avis(id_film=id_film)

    def obtenir_avis_par_utilisateur(self, utilisateur_pseudo: str) -> list:
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
        avis = Avis(id_avis=None, id_film=id_film,
                    utilisateur=utilisateur_pseudo,
                    commentaire=commentaire, note=note)
        return self.avis_dao.modifier_avis(avis)

    def supprimer_avis(self, id_film: int, utilisateur_pseudo: str) -> bool:
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
        return self.avis_dao.supprimer_avis(id_film=id_film,
                                            utilisateur=utilisateur_pseudo)

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
        if not avis_list or avis_list == "Aucun avis trouvé.":
            return 0.0  # Retourne 0 si aucun avis n'est disponible
        total_notes = sum(avis.note for avis in avis_list)
        return total_notes / len(avis_list)
        return total_notes / len(avis_list)
