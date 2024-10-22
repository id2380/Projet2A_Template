from src.dao.avis_dao import AvisDAO
from src.business_object.avis import Avis
from src.business_object.film import Film
from src.business_object.utilisateur import Utilisateur

class AvisService:
    def __init__(self, avis_dao: AvisDAO):
        self.avis_dao = avis_dao

    def ajouter_avis(self,id, film, utilisateur,commentaire, note ) -> Avis:
        """Ajoute un nouvel avis via le DAO."""
        nouvel_avis = Avis(id_avis=id, film = film, utilisateur=utilisateur, note=note, commentaire=commentaire)
        avis_dao = AvisDAO()
        return nouvel_avis if avis_dao.creer_avis(nouvel_avis) else None


    def obtenir_avis_par_film(self, film: Film) -> list:
        """Obtient tous les avis pour un film donné."""
        return self.avis_dao.lire_avis(film=film.titre)  # Utiliser le titre du film, pas l'id

    def obtenir_avis_par_utilisateur(self, utilisateur: Utilisateur) -> list:
        """Obtient tous les avis rédigés par un utilisateur donné."""
        return self.avis_dao.lire_avis(utilisateur=utilisateur.pseudo)  # Utiliser le pseudo de l'utilisateur

    def modifier_avis(self, avis: Avis) -> bool:
        """Modifie un avis existant via le DAO."""
        return self.avis_dao.modifier_avis(avis)

    def supprimer_avis(self, avis_id: int) -> bool:
        """Supprime un avis via le DAO."""
        return self.avis_dao.supprimer_avis(avis_id)

    def calculer_note_moyenne(self, film: Film) -> float:
        """Calcule la note moyenne des avis pour un film spécifié."""
        avis_list = self.avis_dao.lire_avis(film=film.titre)  # Utiliser le titre du film, pas l'id
        if not avis_list:
            return 0.0  # Retourne 0 si aucun avis n'est disponible
        total_notes = sum(avis.note for avis in avis_list)
        return total_notes / len(avis_list) if avis_list else 0.0
