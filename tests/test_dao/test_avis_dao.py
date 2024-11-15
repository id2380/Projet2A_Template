from src.dao.avis_dao import AvisDAO
from src.dao.film_dao import FilmDAO
from src.Model.film import Film
from src.dao.utilisateur_dao import UtilisateurDAO
from src.Model.avis import Avis
from src.Model.utilisateur import Utilisateur


class TestAvisDao:
    """
    Classe de tests pour les fonctionnalités de AvisDAO.
    """

    def setup_method(self):
        """Initialise les données nécessaires pour les tests."""
        self.avis_dao = AvisDAO()
        self.utilisateur_dao = UtilisateurDAO()
        self.film_dao = FilmDAO()

        # Supprimer les données de test existantes
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
            id_film=14918,
            titre="Film Test",
            genres=["Aventure"],
            date_de_sortie="2023-01-01",
            langue_originale="FR",
            synopsis="Synopsis du film test"
        )
        if not self.film_dao.existe_film(self.film.id_film):
            self.film_dao.creer_film(self.film)

    def teardown_method(self):
        """Nettoie les données de test après chaque test."""
        self.cleanup_database()

    def cleanup_database(self):
        """Supprime les avis et utilisateurs ajoutés pour éviter les conflits."""
        utilisateurs = ["utilisateur_test", "autre_utilisateur"]
        for pseudo in utilisateurs:
            utilisateur = self.utilisateur_dao.chercher_utilisateur_par_pseudo(pseudo)
            if utilisateur:
                self.avis_dao.supprimer_avis(utilisateur.id_utilisateur, self.film.id_film)
                self.utilisateur_dao.supprimer_utilisateur(utilisateur.id_utilisateur)

    def test_creer_avis(self):
        """Test de création d'un avis."""
        avis = Avis(
            id_film=self.film.id_film,
            id_utilisateur=self.utilisateur_id,
            note=4,
            commentaire="Bon film"
        )
        self.avis_dao.creer_avis(avis)
        avis_list = self.avis_dao.lire_avis(id_film=self.film.id_film)
        assert len(avis_list) == 1
        assert avis_list[0].note == 4

    def test_modifier_avis(self):
        """Test de modification d'un avis."""
        avis = Avis(
            id_film=self.film.id_film,
            id_utilisateur=self.utilisateur_id,
            note=5,
            commentaire="Excellent!"
        )
        self.avis_dao.creer_avis(avis)

        # Modifier l'avis
        avis.note = 3
        avis.commentaire = "Film correct"
        self.avis_dao.modifier_avis(avis)

        # Vérifier la modification
        avis_modifie = self.avis_dao.lire_avis(id_film=self.film.id_film, id_utilisateur=self.utilisateur_id)
        assert avis_modifie[0].note == 3
        assert avis_modifie[0].commentaire == "Film correct"

    def test_supprimer_avis(self):
        """Test de suppression d'un avis."""
        avis = Avis(
            id_film=self.film.id_film,
            id_utilisateur=self.utilisateur_id,
            note=4,
            commentaire="Film moyen"
        )
        self.avis_dao.creer_avis(avis)
        self.avis_dao.supprimer_avis(self.film.id_film, self.utilisateur_id)
        avis_list = self.avis_dao.lire_avis(id_film=self.film.id_film, id_utilisateur=self.utilisateur_id)
        assert len(avis_list) == 0

    def test_lire_avis_existant(self):
        """Test pour lire un avis existant."""
        avis = Avis(
            id_film=self.film.id_film,
            id_utilisateur=self.utilisateur_id,
            note=5,
            commentaire="Excellent!"
        )
        self.avis_dao.creer_avis(avis)
        avis_list = self.avis_dao.lire_avis(id_film=self.film.id_film)
        assert len(avis_list) == 1
        assert avis_list[0].note == 5

    def test_lire_avis_inexistant(self):
        """Test pour lire un avis inexistant."""
        avis_list = self.avis_dao.lire_avis(id_film=999999)  # ID de film inexistant
        assert len(avis_list) == 0

    def test_lire_tous_avis_pour_film(self):
        """Test pour lire tous les avis liés à un film."""
        autre_utilisateur = Utilisateur(
            pseudo="autre_utilisateur",
            adresse_email="autre@exemple.com",
            mot_de_passe="password456",
            sel="autreSel"
        )
        self.utilisateur_dao.creer(autre_utilisateur)
        autre_utilisateur_id = self.utilisateur_dao.chercher_utilisateur_par_pseudo("autre_utilisateur").id_utilisateur

        avis1 = Avis(
            id_film=self.film.id_film,
            id_utilisateur=self.utilisateur_id,
            note=4,
            commentaire="Bon film"
        )
        avis2 = Avis(
            id_film=self.film.id_film,
            id_utilisateur=autre_utilisateur_id,
            note=5,
            commentaire="Très bon film"
        )
        self.avis_dao.creer_avis(avis1)
        self.avis_dao.creer_avis(avis2)

        avis_list = self.avis_dao.lire_avis(id_film=self.film.id_film)
        assert len(avis_list) == 2

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
