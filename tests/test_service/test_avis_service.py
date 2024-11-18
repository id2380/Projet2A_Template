import pytest
from src.service.avis_service import AvisService
from src.service.eclaireur_service import EclaireurService
from src.dao.utilisateur_dao import UtilisateurDAO
from src.dao.avis_dao import AvisDAO
from src.dao.film_dao import FilmDAO
from src.Model.utilisateur import Utilisateur
from src.Model.avis import Avis
from src.Model.film import Film


class TestAvisService:
    def setup_method(self):
        """Initialise les données nécessaires pour les tests"""
        self.avis_service = AvisService()
        self.eclaireur_service = EclaireurService()
        self.utilisateur_dao = UtilisateurDAO()
        self.film_dao = FilmDAO()
        self.avis_dao = AvisDAO()

        # Nettoyage des données de test
        self.cleanup_database()

        # Créer des utilisateurs de test
        self.utilisateur1 = Utilisateur(
            pseudo="utilisateur1",
            adresse_email="utilisateur1@test.com",
            mot_de_passe="password123",
            sel="sel123"
        )
        self.utilisateur2 = Utilisateur(
            pseudo="utilisateur2",
            adresse_email="utilisateur2@test.com",
            mot_de_passe="password456",
            sel="sel456"
        )
        self.utilisateur_dao.creer(self.utilisateur1)
        self.utilisateur_dao.creer(self.utilisateur2)

        self.utilisateur1_id = self.utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur1").id_utilisateur
        self.utilisateur2_id = self.utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur2").id_utilisateur

        # Créer un film de test
        self.film = Film(
            id_film=12345,
            titre="Film Test",
            genres=["Action"],
            date_de_sortie="2023-01-01",
            langue_originale="FR",
            synopsis="Un film test"
        )
        if not self.film_dao.existe_film(self.film.id_film):
            self.film_dao.creer_film(self.film)

    def teardown_method(self):
        """Nettoie les données après chaque test"""
        self.cleanup_database()

    def cleanup_database(self):
        """Supprime les données créées pendant les tests"""
        # Supprimer tous les avis associés au film de test
        avis = self.avis_dao.lire_avis(id_film=12345)
        for a in avis:
            self.avis_dao.supprimer_avis(id_film=12345, id_utilisateur=a.id_utilisateur)

        # Supprimer les utilisateurs de test
        utilisateurs = ["utilisateur1", "utilisateur2"]
        for pseudo in utilisateurs:
            user = self.utilisateur_dao.chercher_utilisateur_par_pseudo(pseudo)
            if user:
                self.utilisateur_dao.supprimer_utilisateur(user.id_utilisateur)

        # Supprimer le film de test
        if self.film_dao.existe_film(12345):
            self.film_dao.supprimer_film(12345)

    def test_ajouter_avis(self):
        """Test pour ajouter un avis"""
        self.avis_service.ajouter_avis(self.film.id_film, self.utilisateur1_id, 5, "Excellent film")
        avis = self.avis_dao.lire_avis(self.film.id_film, self.utilisateur1_id)
        assert len(avis) == 1
        assert avis[0].note == 5
        assert avis[0].commentaire == "Excellent film"

    def test_obtenir_avis(self):
        """Test pour obtenir les avis d'un film"""
        self.avis_service.ajouter_avis(self.film.id_film, self.utilisateur1_id, 4, "Bon film")
        avis = self.avis_service.obtenir_avis(id_film=self.film.id_film)
        assert len(avis) == 1
        assert avis[0].note == 4
        assert avis[0].commentaire == "Bon film"

    def test_modifier_avis(self):
        """Test pour modifier un avis existant"""
        self.avis_service.ajouter_avis(self.film.id_film, self.utilisateur1_id, 4, "Bon film")
        self.avis_service.modifier_avis(self.film.id_film, self.utilisateur1_id, 5, "Meilleur film")
        avis = self.avis_dao.lire_avis(self.film.id_film, self.utilisateur1_id)
        assert avis[0].note == 5
        assert avis[0].commentaire == "Meilleur film"

    def test_supprimer_avis(self):
        """Test pour supprimer un avis"""
        self.avis_service.ajouter_avis(self.film.id_film, self.utilisateur1_id, 3, "Film moyen")
        self.avis_service.supprimer_avis(self.film.id_film, self.utilisateur1_id)
        avis = self.avis_dao.lire_avis(self.film.id_film, self.utilisateur1_id)
        assert len(avis) == 0

    def test_calculer_note_moyenne(self):
        """Test pour calculer la note moyenne d'un film"""
        self.avis_service.ajouter_avis(self.film.id_film, self.utilisateur1_id, 4, "Bon film")
        self.avis_service.ajouter_avis(self.film.id_film, self.utilisateur2_id, 5, "Excellent film")
        note_moyenne = self.avis_service.calculer_note_moyenne(self.film.id_film)
        assert note_moyenne == 4.5

    def test_lire_avis_eclaireurs(self):
        """Test pour lire les avis des éclaireurs"""
        self.eclaireur_service.ajouter_eclaireur_id(self.utilisateur1_id, self.utilisateur2_id)
        self.avis_service.ajouter_avis(self.film.id_film, self.utilisateur2_id, 4, "Bon film")
        avis = self.avis_service.lire_avis_eclaireurs(self.film.id_film, self.utilisateur1_id)
        assert len(avis) == 1
        assert avis[0].note == 4
        assert avis[0].commentaire == "Bon film"

    def test_calculer_note_moyenne_eclaireurs(self):
        """Test pour calculer la note moyenne des avis des éclaireurs"""
        self.eclaireur_service.ajouter_eclaireur_id(self.utilisateur1_id, self.utilisateur2_id)
        self.avis_service.ajouter_avis(self.film.id_film, self.utilisateur2_id, 5, "Excellent film")
        note_moyenne = self.avis_service.calculer_note_moyenne_eclaireurs(self.film.id_film, self.utilisateur1_id)
        assert note_moyenne == 5.0

    def test_lire_avis_communs(self):
        """Test pour lire les avis communs entre deux utilisateurs"""
        self.avis_service.ajouter_avis(self.film.id_film, self.utilisateur1_id, 4, "Bon film")
        self.avis_service.ajouter_avis(self.film.id_film, self.utilisateur2_id, 5, "Excellent film")
        avis_communs = self.avis_service.lire_avis_communs(self.utilisateur1_id, self.utilisateur2_id)
        assert len(avis_communs) == 1
        assert avis_communs[0]["Avis 1"].note == 4
        assert avis_communs[0]["Avis 2"].note == 5


if __name__ == "__main__":
    pytest.main([__file__])
