from unittest import mock
from unittest.mock import MagicMock

from src.dao.utilisateur_dao import UtilisateurDAO
from src.Model.utilisateur import Utilisateur
from src.Service.eclaireur_service import EclaireurService


class TestEclaireurService:
    import dotenv
    dotenv.load_dotenv(override=True)

    def test_ajouter_eclaireur_id_ok(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        utilisateur = Utilisateur(pseudo="utilisateur",
                                  adresse_email="utilisateur@",
                                  mot_de_passe="mdp_utilisateur",
                                  sel="sel_utilisateur")
        eclaireur = Utilisateur(pseudo="éclaireur",
                                adresse_email="éclaireur@",
                                mot_de_passe="mdp_éclaireur",
                                sel="sel_eclaireur")
        utilisateur_dao.creer(utilisateur)
        utilisateur_dao.creer(eclaireur)
        res = True
        # WHEN
        try:
            EclaireurService().ajouter_eclaireur_id(utilisateur_dao.chercher_utilisateur_par_pseudo(utilisateur.pseudo).id_utilisateur, utilisateur_dao.chercher_utilisateur_par_pseudo(eclaireur.pseudo).id_utilisateur)
        except Exception:
            res = False
        # THEN
        assert res
        
    def test_ajouter_eclaireur_id_inexistant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True
        # WHEN
        try:
            EclaireurService().ajouter_eclaireur_id(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur, 1000)
        except Exception:
            res = False
        # THEN
        assert res is False

    def test_ajouter_eclaireur_id_eclaireur(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True
        # WHEN
        try:
            EclaireurService().ajouter_eclaireur_id(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur, utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur").id_utilisateur)
        except Exception:
            res = False
        # THEN
        assert res is False

    def test_ajouter_eclaireur_pseudo_ok(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        utilisateur3 = Utilisateur(pseudo="utilisateur3",
                                   adresse_email="utilisateur3@",
                                   mot_de_passe="mdp_utilisateur3",
                                   sel="sel_utilisateur3")
        eclaireur3 = Utilisateur(pseudo="éclaireur3",
                                 adresse_email="éclaireur3@",
                                 mot_de_passe="mdp_éclaireur3",
                                 sel="sel_eclaireur3")
        utilisateur_dao.creer(utilisateur3)
        utilisateur_dao.creer(eclaireur3)
        res = True
        # WHEN
        try:
            EclaireurService().ajouter_eclaireur_pseudo(utilisateur_dao.chercher_utilisateur_par_pseudo(utilisateur3.pseudo).id_utilisateur, eclaireur3.pseudo)
        except Exception:
            res = False
        # THEN
        assert res
        
    def test_ajouter_eclaireur_pseudo_inexistant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True
        # WHEN
        try:
            EclaireurService().ajouter_eclaireur_pseudo(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "éclaireur4")
        except Exception:
            res = False
        # THEN
        assert res is False

    def test_ajouter_eclaireur_pseudo_eclaireur(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True
        # WHEN
        try:
            EclaireurService().ajouter_eclaireur_pseudo(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "éclaireur3")
        except Exception:
            res = False
        # THEN
        assert res is False

    def test_est_eclaireur_id_true(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        # WHEN
        try:
            res = EclaireurService().est_eclaireur_id(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur, utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur").id_utilisateur)
        except Exception:
            res = None
        # THEN
        assert res
    
    def test_est_eclaireur_id_false(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        # WHEN
        try:
            res = EclaireurService().est_eclaireur_id(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur, utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur)
        except Exception:
            res = None
        # THEN
        assert res is False

    def test_est_eclaireur_id_inexistant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        # WHEN
        try:
            res = EclaireurService().est_eclaireur_id(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur, 1000)
        except Exception:
            res = None
        # THEN
        assert res is None

    def test_est_eclaireur_pseudo_true(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        # WHEN
        try:
            res = EclaireurService().est_eclaireur_pseudo(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "éclaireur3")
        except Exception:
            res = None
        # THEN
        assert res
    
    def test_est_eclaireur_pseudo_false(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        # WHEN
        try:
            res = EclaireurService().est_eclaireur_pseudo(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "utilisateur")
        except Exception:
            res = None
        # THEN
        assert res is False

    def test_est_eclaireur_pseudo_inexistant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        # WHEN
        try:
            res = EclaireurService().est_eclaireur_pseudo(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "éclaireur2")
        except Exception:
            res = None
        # THEN
        assert res is None

    def test_liste_eclaireurs_existant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        # WHEN
        res = EclaireurService().liste_eclaireurs(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur)
        # THEN
        assert len(res) > 0

    def test_liste_eclaireurs_inexistant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        # WHEN
        res = EclaireurService().liste_eclaireurs(utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur").id_utilisateur)
        # THEN
        assert len(res) == 0

    def test_supprimer_eclaireur_id_ok(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True
        # WHEN
        try:
            EclaireurService().supprimer_eclaireur_id(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur, utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur").id_utilisateur)
        except Exception:
            res = False
        # THEN
        assert res
        
    def test_supprimer_eclaireur_id_inexistant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True
        # WHEN
        try:
            EclaireurService().supprimer_eclaireur_id(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur, 1000)
        except Exception:
            res = False
        # THEN
        assert res is False

    def test_supprimer_eclaireur_id_eclaireur(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True
        # WHEN
        try:
            EclaireurService().supprimer_eclaireur_id(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur, utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur").id_utilisateur)
        except Exception:
            res = False
        # THEN
        assert res is False

    def test_supprimer_eclaireur_pseudo_ok(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True
        # WHEN
        try:
            EclaireurService().supprimer_eclaireur_pseudo(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "éclaireur3")
        except Exception:
            res = False
        # THEN
        assert res
        
    def test_supprimer_eclaireur_pseudo_inexistant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True
        # WHEN
        try:
            EclaireurService().supprimer_eclaireur_id(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "éclaireur2")
        except Exception:
            res = False
        # THEN
        assert res is False

    def test_supprimer_eclaireur_pseudo_eclaireur(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True
        # WHEN
        try:
            EclaireurService().supprimer_eclaireur_pseudo(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "éclaireur3")
        except Exception:
            res = False
        # THEN
        assert res is False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
