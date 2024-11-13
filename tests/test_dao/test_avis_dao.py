from src.dao.avis_dao import AvisDAO
from src.dao.film_dao import FilmDAO
from src.business_object.film import Film    
from src.dao.utilisateur_dao import UtilisateurDAO
from src.business_object.avis import Avis
from src.Model.utilisateur import Utilisateur


class TestAvisDao:
    """
    Classe de tests pour les fonctionnalités de AvisDAO.
    """

    def test_creer_avis(self):
        # GIVEN
        avis_dao = AvisDAO()
        utilisateur_dao = UtilisateurDAO()
        film_dao = FilmDAO()

        # Créer utilisateur et film pour les tests
        utilisateur = Utilisateur(
            pseudo="utilisateur_test", adresse_email="utilisateur@test.com",
            mot_de_passe="password123", sel="sel123"
        )
        utilisateur_dao.creer(utilisateur)
        id_utilisateur = utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur_test").id_utilisateur
        
        # Créer un objet Film au lieu d'un ID
        film = Film(
            id_film=14918,
            titre="Film Test",
            genres={"Aventure"},
            date_de_sortie="2023-01-01",
            langue_originale="FR",
            synopsis="Synopsis du film test"
        )
        film_dao.creer_film(film)  # Passer l'objet Film à la place de l'ID

        # Créer un avis lié à cet utilisateur et ce film
        avis = Avis(id_avis=None, id_film=film.id_film, utilisateur="utilisateur_test", note=4, commentaire="Bon film")
        res = avis_dao.creer_avis(avis)

        # THEN
        assert res
    def test_modifier_avis(self):
        # GIVEN
        avis_dao = AvisDAO()
        utilisateur_dao = UtilisateurDAO()
        utilisateur_id = utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur_test").id_utilisateur

        avis = Avis(id_avis=None, id_film=1184918, utilisateur="utilisateur_test", note=5, commentaire="Excellent!")
        avis_dao.creer_avis(avis)

        # WHEN
        avis.note = 3
        avis.commentaire = "Film correct"
        res = avis_dao.modifier_avis(avis)

        # THEN
        assert res

    def test_supprimer_avis(self):
        # GIVEN
        avis_dao = AvisDAO()
        utilisateur_dao = UtilisateurDAO()
        utilisateur_id = utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur_test").id_utilisateur

        avis = Avis(id_avis=None, id_film=1184918, utilisateur="utilisateur_test", note=4, commentaire="Film moyen")
        avis_dao.creer_avis(avis)

        # WHEN
        res = avis_dao.supprimer_avis(utilisateur="utilisateur_test", id_film=1184918)

        # THEN
        assert res

    def test_lire_avis_existant(self):
        # GIVEN
        avis_dao = AvisDAO()
        utilisateur_dao = UtilisateurDAO()

        # WHEN
        avis_list = avis_dao.lire_avis(id_film=14918, utilisateur="utilisateur_test")

        # THEN
        assert len(avis_list) > 0

    def test_lire_avis_inexistant(self):
        # GIVEN
        avis_dao = AvisDAO()

        # WHEN
        avis_list = avis_dao.lire_avis(id_film=9999999)  # ID de film non existant

        # THEN
        assert avis_list == []

    def test_lire_tous_avis_pour_film(self):
        # GIVEN
        avis_dao = AvisDAO()
        utilisateur_dao = UtilisateurDAO()
        utilisateur_dao.creer(Utilisateur(
            pseudo="autre_utilisateur", adresse_email="autre@exemple.com",
            mot_de_passe="autre123", sel="autreSel"
        ))

        avis1 = Avis(id_avis=None, id_film=1184918, utilisateur="utilisateur_test", note=4, commentaire="Bon film")
        avis2 = Avis(id_avis=None, id_film=1184918, utilisateur="autre_utilisateur", note=5, commentaire="Très bon film")
        avis_dao.creer_avis(avis1)
        avis_dao.creer_avis(avis2)

        # WHEN
        avis_list = avis_dao.lire_avis(id_film=1184918)

        # THEN
        assert len(avis_list) >= 2

    def test_supprimer_avis_et_utilisateurs(self):
        # Supprimer tous les avis et utilisateurs créés pour les tests.
        utilisateur_dao = UtilisateurDAO()
        utilisateur_dao.supprimer_utilisateur(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur_test").id_utilisateur)
        utilisateur_dao.supprimer_utilisateur(utilisateur_dao.chercher_utilisateur_par_pseudo("autre_utilisateur").id_utilisateur)

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
