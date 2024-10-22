from datetime import datetime
from src.business_object.avis import Avis
from src.business_object.film import Film
from src.business_object.utilisateur import Utilisateur
from src.dao.utilisateur_dao import UtilisateurDAO
from src.dao.film_dao import FilmDAO
from src.dao.avis_dao import AvisDAO


class TestAvisDAO:
    def inserer_donnees_test():
        """Insère un film et un utilisateur de test dans la base de données."""
        film_dao = FilmDAO()
        utilisateur_dao = UtilisateurDAO()

        # Ajout du film
        film = Film(
            id_film=1,
            titre="La Reine des Neiges",
            genre="Animation",
            date_de_sortie=datetime(2013, 11, 27),
            langue_originale="Français",
            synopsis="Un film d'animation sur une princesse et ses pouvoirs de glace."
        )
        film_dao.creer_film(film)

        # Ajout de l'utilisateur
        utilisateur = Utilisateur(
            id_utilisateur=1,
            pseudo="Soukayna",
            email="soukayna.hessane@eleve.ensai.fr",
            mot_de_passe="securepassword"
        )
        utilisateur_dao.creer_utilisateur(utilisateur)
    inserer_donnees_test()
    def test_create_avis_ok(self):
        # GIVEN
        avis_dao = AvisDAO()
        avis = Avis(
            id_avis=None,
            film="La Reine des Neiges",
            utilisateur="Soukayna",
            note=5,
            commentaire="Film incroyable"
        )

        # WHEN
        created = avis_dao.creer_avis(avis)

        # THEN
        assert created

    def test_create_avis_existant(self):
        # GIVEN
        avis_dao = AvisDAO()
        avis = Avis(
            id_avis=None,
            film="La Reine des Neiges",
            utilisateur="Soukayna",
            note=5,
            commentaire="Film incroyable"
        )

        # WHEN
        created = avis_dao.creer_avis(avis)

        # THEN
        assert created is False

    def test_read_avis_existant(self, avis_id=1):
        # GIVEN
        avis_dao = AvisDAO()

        # WHEN
        read = avis_dao.lire_avis(avis_id=avis_id)

        # THEN
        assert read is not None
        assert len(read) > 0  # Si l'avis existe, il y aura au moins un résultat

    def test_read_avis_inexistant(self, avis_id=999):
        # GIVEN
        avis_dao = AvisDAO()

        # WHEN
        read = avis_dao.lire_avis(avis_id=avis_id)

        # THEN
        assert read == []

    def test_delete_avis_existant(self, avis_id=1):
        # GIVEN
        avis_dao = AvisDAO()

        # WHEN
        deleted = avis_dao.supprimer_avis(avis_id)

        # THEN
        assert deleted is True

    def test_delete_avis_inexistant(self, avis_id=999):
        # GIVEN
        avis_dao = AvisDAO()

        # WHEN
        deleted = avis_dao.supprimer_avis(avis_id)

        # THEN
        assert deleted is False


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
