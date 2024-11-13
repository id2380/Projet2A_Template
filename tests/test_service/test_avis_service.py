from src.business_object.avis import Avis
from src.dao.avis_dao import AvisDAO
from src.service.avis_service import AvisService
from src.Model.utilisateur import Utilisateur
from src.dao.utilisateur_dao import UtilisateurDAO
from src.dao.film_dao import FilmDAO
from src.business_object.film import Film
from src.service.film_service import FilmService

class TestAvisService:
    
    def setup_method(self):
        """Initialise les données nécessaires pour les tests"""
        self.avis_service = AvisService()
        self.utilisateur_dao = UtilisateurDAO()
        self.film_dao = FilmDAO()
        self.avis_dao = AvisDAO()
        self.film_service = FilmService()

        # Supprime les avis et utilisateurs précédents pour éviter les doublons
        self.cleanup_database()

        # Crée un utilisateur pour les tests
        self.utilisateur = Utilisateur(
            pseudo="utilisateur_test",
            adresse_email="utilisateur@test.com",
            mot_de_passe="password123",
            sel="sel123"
        )
        try:
            self.utilisateur_dao.creer(self.utilisateur)
            self.utilisateur_id = self.utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur_test").id_utilisateur
        except Exception:
            pass  # Ignore si l'utilisateur existe déjà

        # Crée un film pour les tests
        if not self.film_service.existe_film(1184918):
            self.film = Film(
                id_film=1184918,
                titre="Film Test",
                genres=["Aventure"],
                date_de_sortie="2023-01-01",
                langue_originale="FR",
                synopsis="Synopsis du film test"
            )
            try:
                self.film_dao.creer_film(self.film)
            except Exception:
                pass  # Ignore si le film existe déjà

    def teardown_method(self):
        """Nettoie la base de données après chaque test"""
        self.cleanup_database()

    def cleanup_database(self):
        """Supprime les avis et utilisateurs ajoutés pour éviter les conflits."""
        # Supprime tous les avis de test
        for utilisateur in ["utilisateur_test", "autre_utilisateur"]:
            while True:
                avis = self.avis_dao.lire_avis(utilisateur=utilisateur)
                if not avis:
                    break
                self.avis_dao.supprimer_avis(id_film=1184918, utilisateur=utilisateur)
        
        # Supprime les utilisateurs de test s'ils existent
        utilisateur_test = self.utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur_test")
        if utilisateur_test:
            self.utilisateur_dao.supprimer_utilisateur(utilisateur_test.id_utilisateur)
        autre_utilisateur = self.utilisateur_dao.chercher_utilisateur_par_pseudo("autre_utilisateur")
        if autre_utilisateur:
            self.utilisateur_dao.supprimer_utilisateur(autre_utilisateur.id_utilisateur)

    def test_ajouter_avis_success(self):
        # WHEN: Ajout d'un avis pour un film existant
        avis = self.avis_service.ajouter_avis(
            id_film=1184918,
            utilisateur="utilisateur_test",
            commentaire="Film incroyable",
            note=5
        )

        # THEN: Vérification de la création de l'avis
        assert avis is not None
        assert avis.id_film == 1184918
        assert avis.utilisateur == "utilisateur_test"
        assert avis.commentaire == "Film incroyable"
        assert avis.note == 5

    def test_calculer_note_moyenne(self):
        # GIVEN: Ajout de plusieurs avis
        self.avis_service.ajouter_avis(
            id_film=1184918,
            utilisateur="utilisateur_test",
            commentaire="Film incroyable",
            note=5
        )
        autre_utilisateur = Utilisateur(
            pseudo="autre_utilisateur",
            adresse_email="autre@test.com",
            mot_de_passe="password456",
            sel="sel456"
        )
        try:
            self.utilisateur_dao.creer(autre_utilisateur)
        except Exception:
            pass  # Ignore si l'utilisateur existe déjà
        self.avis_service.ajouter_avis(
            id_film=1184918,
            utilisateur="autre_utilisateur",
            commentaire="Bon film",
            note=3
        )

        # WHEN: Calcul de la note moyenne
        note_moyenne = self.avis_service.calculer_note_moyenne(id_film=1184918)
        
        # THEN: Vérification du calcul correct
        assert note_moyenne == 4.0

    def test_modifier_avis_success(self):
        # GIVEN: Crée un avis
        self.avis_service.ajouter_avis(
            id_film=1184918,
            utilisateur="utilisateur_test",
            commentaire="Film incroyable",
            note=5
        )

        # WHEN: Modifie l'avis existant
        resultat = self.avis_service.modifier_avis(
            id_film=1184918,
            utilisateur="utilisateur_test",
            commentaire="Très bon film",
            note=4
        )

        # THEN: Vérification de la modification de l'avis
        assert resultat is True

    def test_supprimer_avis_success(self):
        # GIVEN: Ajoute un avis pour pouvoir le supprimer
        self.avis_service.ajouter_avis(
            id_film=1184918,
            utilisateur="utilisateur_test",
            commentaire="Film incroyable",
            note=5
        )

        # WHEN: Supprime l'avis
        resultat = self.avis_service.supprimer_avis(
            id_film=1184918,
            utilisateur="utilisateur_test"
        )

        # THEN: Vérifie la suppression de l'avis
        assert resultat is True
    
    def test_obtenir_avis(self):
        # GIVEN: Ajout d'avis pour plusieurs utilisateurs
        self.avis_service.ajouter_avis(
            id_film=1184918,
            utilisateur="utilisateur_test",
            commentaire="Film incroyable",
            note=5
        )
        autre_utilisateur = Utilisateur(
            pseudo="autre_utilisateur",
            adresse_email="autre@test.com",
            mot_de_passe="password456",
            sel="sel456"
        )
        try:
            self.utilisateur_dao.creer(autre_utilisateur)
        except Exception:
            pass
        self.avis_service.ajouter_avis(
            id_film=1184918,
            utilisateur="autre_utilisateur",
            commentaire="Bon film",
            note=3
        )

        # WHEN: Récupérer les avis par `id_film` seulement
        avis_par_film = self.avis_service.obtenir_avis(id_film=1184918)
        
        # THEN: Vérifier que les deux avis sont bien récupérés
        assert len(avis_par_film) == 2

        # WHEN: Récupérer l'avis par utilisateur seulement
        avis_par_utilisateur = self.avis_service.obtenir_avis(utilisateur="utilisateur_test")
        
        # THEN: Vérifier que l'avis de "utilisateur_test" est bien récupéré
        assert len(avis_par_utilisateur) == 1
        assert avis_par_utilisateur[0]['utilisateur'] == "utilisateur_test"
        assert avis_par_utilisateur[0]['note'] == 5

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
