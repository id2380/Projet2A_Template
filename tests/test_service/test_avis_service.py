from src.service.avis_service import AvisService
from src.dao.utilisateur_dao import UtilisateurDAO
from src.dao.film_dao import FilmDAO
from src.Model.avis import Avis
from src.Model.utilisateur import Utilisateur
from src.Model.film import Film
from src.dao.avis_dao import AvisDAO

class TestAvisService:

    def setup_method(self):
        """Initialise les données nécessaires pour les tests"""
        self.avis_service = AvisService()
        self.utilisateur_dao = UtilisateurDAO()
        self.film_dao = FilmDAO()
        self.avis_dao = AvisDAO()

        # Nettoyer la base de données pour éviter les conflits
        self.cleanup_database()

        # Créer un utilisateur de test
        self.utilisateur = Utilisateur(
            pseudo="utilisateur_test",
            adresse_email="utilisateur@test.com",
            mot_de_passe="password123",
            sel="sel123"
        )
        self.utilisateur_dao.creer(self.utilisateur)
        self.utilisateur_id = self.utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur_test").id_utilisateur

        # Créer un film de test
        self.film = Film(
            id_film=1184918,
            titre="Film Test",
            genres=["Aventure"],
            date_de_sortie="2023-01-01",
            langue_originale="FR",
            synopsis="Synopsis du film test"
        )
        if not self.film_dao.existe_film(self.film.id_film):
            self.film_dao.creer_film(self.film)

    def teardown_method(self):
        """Nettoie la base de données après chaque test"""
        self.cleanup_database()

    def cleanup_database(self):
        """Supprime les données de test pour éviter les conflits"""
        # Supprimer les avis de test
        for utilisateur in ["utilisateur_test", "autre_utilisateur"]:
            user = self.utilisateur_dao.chercher_utilisateur_par_pseudo(utilisateur)
            if user:
                self.avis_dao.supprimer_avis(id_film=1184918, id_utilisateur=user.id_utilisateur)

        # Supprimer les utilisateurs de test
        for utilisateur in ["utilisateur_test", "autre_utilisateur"]:
            user = self.utilisateur_dao.chercher_utilisateur_par_pseudo(utilisateur)
            if user:
                self.utilisateur_dao.supprimer_utilisateur(user.id_utilisateur)

    def test_ajouter_avis_success(self):
        """Test pour ajouter un avis avec succès"""
        avis = Avis(
            id_film=1184918,
            id_utilisateur=self.utilisateur_id,
            note=5,
            commentaire="Film incroyable"
        )
        self.avis_service.ajouter_avis(avis.id_film, avis.id_utilisateur, avis.note, avis.commentaire)
        avis_recupere = self.avis_dao.lire_avis(id_film=avis.id_film, id_utilisateur=avis.id_utilisateur)
        assert len(avis_recupere) == 1
        assert avis_recupere[0].commentaire == "Film incroyable"

    def test_calculer_note_moyenne(self):
        """Test pour calculer la note moyenne d'un film"""
        self.avis_service.ajouter_avis(1184918, self.utilisateur_id, 5, "Excellent")
        autre_utilisateur = Utilisateur(
            pseudo="autre_utilisateur",
            adresse_email="autre@test.com",
            mot_de_passe="password456",
            sel="sel456"
        )
        self.utilisateur_dao.creer(autre_utilisateur)
        autre_utilisateur_id = self.utilisateur_dao.chercher_utilisateur_par_pseudo("autre_utilisateur").id_utilisateur
        self.avis_service.ajouter_avis(1184918, autre_utilisateur_id, 3, "Bon film")
        note_moyenne = self.avis_service.calculer_note_moyenne(1184918)
        assert note_moyenne == 4.0

    def test_modifier_avis_success(self):
        """Test pour modifier un avis avec succès"""
        self.avis_service.ajouter_avis(1184918, self.utilisateur_id, 5, "Excellent")
        self.avis_service.modifier_avis(1184918, self.utilisateur_id, 4, "Bon film")
        avis = self.avis_dao.lire_avis(1184918, self.utilisateur_id)
        assert avis[0].note == 4
        assert avis[0].commentaire == "Bon film"

    def test_supprimer_avis_success(self):
        """Test pour supprimer un avis avec succès"""
        self.avis_service.ajouter_avis(1184918, self.utilisateur_id, 5, "Excellent")
        self.avis_service.supprimer_avis(1184918, self.utilisateur_id)
        avis = self.avis_dao.lire_avis(1184918, self.utilisateur_id)
        assert len(avis) == 0

    def test_obtenir_avis(self):
        """Test pour obtenir des avis"""
        self.avis_service.ajouter_avis(1184918, self.utilisateur_id, 5, "Excellent")
        avis = self.avis_service.obtenir_avis(id_film=1184918)
        assert len(avis) == 1
        assert avis[0].commentaire == "Excellent"

    def test_lire_avis_communs(self):
        """Test pour lire les avis communs entre deux utilisateurs"""
        autre_utilisateur = Utilisateur(
            pseudo="autre_utilisateur",
            adresse_email="autre@test.com",
            mot_de_passe="password456",
            sel="sel456"
        )
        self.utilisateur_dao.creer(autre_utilisateur)
        autre_utilisateur_id = self.utilisateur_dao.chercher_utilisateur_par_pseudo("autre_utilisateur").id_utilisateur
        self.avis_service.ajouter_avis(1184918, self.utilisateur_id, 5, "Excellent")
        self.avis_service.ajouter_avis(1184918, autre_utilisateur_id, 4, "Très bon")
        avis_communs = self.avis_service.lire_avis_communs(self.utilisateur_id, autre_utilisateur_id)
        assert len(avis_communs) == 1
        assert avis_communs[0]["Avis 1"].note == 5
        assert avis_communs[0]["Avis 2"].note == 4


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
