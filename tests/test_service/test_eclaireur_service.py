from src.dao.utilisateur_dao import UtilisateurDAO
from src.Model.utilisateur import Utilisateur
from src.service.eclaireur_service import EclaireurService


class TestEclaireurService:
    """
    Une classe qui permet de tester les fonctionnalités de la DAO pour
    les éclaireurs.
    """

    import dotenv
    dotenv.load_dotenv(override=True)

    """
    Teste l'ajout d'un éclaireur dans la base à partir de son identifiant.
    """
    def test_ajouter_eclaireur_id_ok(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        utilisateur = Utilisateur(
            pseudo="utilisateur", adresse_email="utilisateur@",
            mot_de_passe="mdp_utilisateur", sel="sel_utilisateur"
        )
        eclaireur = Utilisateur(
            pseudo="éclaireur", adresse_email="éclaireur@",
            mot_de_passe="mdp_éclaireur", sel="sel_eclaireur"
        )
        utilisateur_dao.creer(utilisateur)
        utilisateur_dao.creer(eclaireur)
        res = True

        # WHEN
        try:
            EclaireurService().ajouter_eclaireur_id(
                utilisateur_dao.chercher_utilisateur_par_pseudo(utilisateur.pseudo).id_utilisateur,
                utilisateur_dao.chercher_utilisateur_par_pseudo(eclaireur.pseudo).id_utilisateur,
            )
        except Exception:
            res = False

        # THEN
        assert res

    """
    Teste l'ajout d'un éclaireur dans la base à partir de son identifiant
    si l'éclaireur n'existe pas.
    """
    def test_ajouter_eclaireur_id_inexistant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True

        # WHEN
        try:
            EclaireurService().ajouter_eclaireur_id(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur, 1000
            )
        except Exception:
            res = False

        # THEN
        assert res is False

    """
    Teste l'ajout d'un éclaireur dans la base à partir de son identifiant
    si l'éclaireur a déjà été ajouté.
    """
    def test_ajouter_eclaireur_id_eclaireur(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True

        # WHEN
        try:
            EclaireurService().ajouter_eclaireur_id(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur,
                utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur").id_utilisateur,
            )
        except Exception:
            res = False

        # THEN
        assert res is False

    """
    Teste l'ajout d'un éclaireur dans la base à partir de son pseudo.
    """
    def test_ajouter_eclaireur_pseudo_ok(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        utilisateur3 = Utilisateur(
            pseudo="utilisateur3",
            adresse_email="utilisateur3@",
            mot_de_passe="mdp_utilisateur3",
            sel="sel_utilisateur3",
        )
        eclaireur3 = Utilisateur(
            pseudo="éclaireur3", adresse_email="éclaireur3@", mot_de_passe="mdp_éclaireur3", sel="sel_eclaireur3"
        )
        utilisateur_dao.creer(utilisateur3)
        utilisateur_dao.creer(eclaireur3)
        res = True

        # WHEN
        try:
            EclaireurService().ajouter_eclaireur_pseudo(
                utilisateur_dao.chercher_utilisateur_par_pseudo(utilisateur3.pseudo).id_utilisateur, eclaireur3.pseudo
            )
        except Exception:
            res = False

        # THEN
        assert res

    """
    Teste l'ajout d'un éclaireur dans la base à partir de son pseudo
    si l'éclaireur n'existe pas.
    """
    def test_ajouter_eclaireur_pseudo_inexistant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True

        # WHEN
        try:
            EclaireurService().ajouter_eclaireur_pseudo(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "éclaireur4"
            )
        except Exception:
            res = False

        # THEN
        assert res is False

    """
    Teste l'ajout d'un éclaireur dans la base à partir de son pseudo
    si l'éclaireur a déjà été ajouté.
    """
    def test_ajouter_eclaireur_pseudo_eclaireur(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True

        # WHEN
        try:
            EclaireurService().ajouter_eclaireur_pseudo(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "éclaireur3"
            )
        except Exception:
            res = False

        # THEN
        assert res is False

    """
    Teste la fonction est_eclaireur_id dans le cas où le retour doit être True.
    """
    def test_est_eclaireur_id_true(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()

        # WHEN
        try:
            res = EclaireurService().est_eclaireur_id(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur,
                utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur").id_utilisateur,
            )
        except Exception:
            res = None

        # THEN
        assert res

    """
    Teste la fonction est_eclaireur_id dans le cas où le retour doit être
    False.
    """
    def test_est_eclaireur_id_false(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()

        # WHEN
        try:
            res = EclaireurService().est_eclaireur_id(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur,
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur,
            )
        except Exception:
            res = None

        # THEN
        assert res is False

    """
    Teste la fonction est_eclaireur_id dans le cas où l'éclaireur n'existe pas.
    """
    def test_est_eclaireur_id_inexistant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()

        # WHEN
        try:
            res = EclaireurService().est_eclaireur_id(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur, 1000
            )
        except Exception:
            res = None

        # THEN
        assert res is None

    """
    Teste la fonction est_eclaireur_pseudo dans le cas où le retour doit être
    True.
    """
    def test_est_eclaireur_pseudo_true(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()

        # WHEN
        try:
            res = EclaireurService().est_eclaireur_pseudo(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "éclaireur3"
            )
        except Exception:
            res = None

        # THEN
        assert res

    """
    Teste la fonction est_eclaireur_pseudo dans le cas où le retour doit être False.
    """
    def test_est_eclaireur_pseudo_false(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()

        # WHEN
        try:
            res = EclaireurService().est_eclaireur_pseudo(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "utilisateur"
            )
        except Exception:
            res = None

        # THEN
        assert res is False

    """
    Teste la fonction est_eclaireur_pseudo dans le cas où l'éclaire n'existe
    pas.
    """
    def test_est_eclaireur_pseudo_inexistant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()

        # WHEN
        try:
            res = EclaireurService().est_eclaireur_pseudo(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "éclaireur2"
            )
        except Exception:
            res = None

        # THEN
        assert res is None

    """
    Teste la fonction liste_eclaireur quand l'utilisateur possède des
    éclaireurs.
    """
    def test_liste_eclaireurs_existant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()

        # WHEN
        res = EclaireurService().liste_eclaireurs(
            utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur
        )

        # THEN
        assert len(res) > 0

    """
    Teste la fonction liste_eclaireur quand l'utilisateur ne possède pas d'
    éclaireur.
    """
    def test_liste_eclaireurs_inexistant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()

        # WHEN
        res = EclaireurService().liste_eclaireurs(
            utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur").id_utilisateur
        )

        # THEN
        assert len(res) == 0

    """
    Teste la suppression d'un éclaireur à partir de son identifiant.
    """
    def test_supprimer_eclaireur_id_ok(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True

        # WHEN
        try:
            EclaireurService().supprimer_eclaireur_id(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur,
                utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur").id_utilisateur,
            )
        except Exception:
            res = False

        # THEN
        assert res

    """
    Teste la suppression d'un éclaireur à partir de son identifiant dans le
    cas où il n'existe pas.
    """
    def test_supprimer_eclaireur_id_inexistant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True
        # WHEN
        try:
            EclaireurService().supprimer_eclaireur_id(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur, 1000
            )
        except Exception:
            res = False
        # THEN
        assert res is False

    """
    Teste la suppression d'un éclaireur à partir de son identifiant dans le
    cas où il n'est pas l'éclaireur de l'utilisateur.
    """
    def test_supprimer_eclaireur_id_eclaireur(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True
        # WHEN
        try:
            EclaireurService().supprimer_eclaireur_id(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur,
                utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur").id_utilisateur,
            )
        except Exception:
            res = False
        # THEN
        assert res is False

    """
    Teste la suppression d'un éclaireur à partir de son pseudo.
    """
    def test_supprimer_eclaireur_pseudo_ok(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True
        # WHEN
        try:
            EclaireurService().supprimer_eclaireur_pseudo(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "éclaireur3"
            )
        except Exception:
            res = False
        # THEN
        assert res

    """
    Teste la suppression d'un éclaireur à partir de son pseudo dans le
    cas où il n'existe pas.
    """
    def test_supprimer_eclaireur_pseudo_inexistant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True
        # WHEN
        try:
            EclaireurService().supprimer_eclaireur_id(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "éclaireur2"
            )
        except Exception:
            res = False
        # THEN
        assert res is False

    """
    Teste la suppression d'un éclaireur à partir de son pseudo dans le
    cas où il n'est pas l'éclaireur de l'utilisateur.
    """
    def test_supprimer_eclaireur_pseudo_eclaireur(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        res = True
        # WHEN
        try:
            EclaireurService().supprimer_eclaireur_pseudo(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur, "éclaireur3"
            )
        except Exception:
            res = False
        # THEN
        utilisateur_dao.supprimer_utilisateur(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur)
        utilisateur_dao.supprimer_utilisateur(utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur").id_utilisateur)
        utilisateur_dao.supprimer_utilisateur(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur3").id_utilisateur)
        utilisateur_dao.supprimer_utilisateur(utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur3").id_utilisateur)
        assert res is False


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
