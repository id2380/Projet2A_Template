from src.dao.eclaireur_dao import EclaireurDAO
from src.dao.utilisateur_dao import UtilisateurDAO
from src.Model.utilisateur import Utilisateur


class TestEclaireurDao:
    """
    Une classe qui permet de tester les fonctionnalités de la DAO pour
    les éclaireurs.
    """

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    """
    Teste l'ajout d'un éclaireur dans la base.
    """
    def test_ajouter_eclaireur(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        eclaireur_dao = EclaireurDAO()
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
            eclaireur_dao.ajouter_eclaireur(
                utilisateur_dao.chercher_utilisateur_par_pseudo(utilisateur.pseudo).id_utilisateur,
                utilisateur_dao.chercher_utilisateur_par_pseudo(eclaireur.pseudo).id_utilisateur,
            )
        except Exception:
            res = False

        # THEN
        assert res

    """
    Teste la fonction est_eclaireur dans le cas où le retour doit être True.
    """
    def test_est_eclaireur_true(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        eclaireur_dao = EclaireurDAO()

        # WHEN
        res = eclaireur_dao.est_eclaireur(
            utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur,
            utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur").id_utilisateur,
        )

        # THEN
        assert res

    """
    Teste la fonction est_eclaireur dans le cas où le retour doit être False.
    """
    def test_est_eclaireur_false(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        eclaireur_dao = EclaireurDAO()
        eclaireur2 = Utilisateur(
            pseudo="éclaireur2", adresse_email="éclaireur2@",
            mot_de_passe="mdp_éclaireur2", sel="sel_eclaireur2"
        )
        utilisateur_dao.creer(eclaireur2)

        # WHEN
        res = eclaireur_dao.est_eclaireur(
            utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur,
            utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur2").id_utilisateur,
        )

        # THEN
        assert res is False

    """
    Teste la fonction liste_eclaireur quand l'utilisateur possède des
    éclaireurs.
    """
    def test_liste_eclaireurs_existant(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        eclaireur_dao = EclaireurDAO()

        # GIVEN
        res = eclaireur_dao.liste_eclaireurs(
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
        eclaireur_dao = EclaireurDAO()

        # WHEN
        res = eclaireur_dao.liste_eclaireurs(
            utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur").id_utilisateur
        )

        # THEN
        assert len(res) == 0

    """
    Teste la suppression d'un éclaireur.
    """
    def test_supprimer_eclaireur(self):
        # GIVEN
        utilisateur_dao = UtilisateurDAO()
        eclaireur_dao = EclaireurDAO()
        res = False

        # WHEN
        try:
            eclaireur_dao.supprimer_eclaireur(
                utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur,
                utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur").id_utilisateur,
            )
            res = True
        except Exception:
            res = False

        # THEN
        utilisateur_dao.supprimer_utilisateur(utilisateur_dao.chercher_utilisateur_par_pseudo("utilisateur").id_utilisateur)
        utilisateur_dao.supprimer_utilisateur(utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur").id_utilisateur)
        utilisateur_dao.supprimer_utilisateur(utilisateur_dao.chercher_utilisateur_par_pseudo("éclaireur2").id_utilisateur)
        assert res


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
