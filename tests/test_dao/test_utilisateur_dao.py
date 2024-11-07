import unittest

from src.dao.utilisateur_dao import UtilisateurDAO
from src.Model.utilisateur import Utilisateur
from src.Service.mot_de_passe_service import creer_sel, hacher_mot_de_passe


class TestUtilisateurDAO(unittest.TestCase):
    def setUp(self):
        self.utilisateur_dao = UtilisateurDAO()

    def test_creer(self):
        """Test de création d'un utilisateur"""
        # GIVEN
        sel = creer_sel()
        mot_de_passe_hash = hacher_mot_de_passe("blablabla", sel)
        utilisateur = Utilisateur(
            pseudo="Jean",
            adresse_email="jean.martin@ensai.fr",
            mot_de_passe=mot_de_passe_hash,
            sel=sel
        )
        # WHEN
        creation_ok = self.utilisateur_dao.creer(utilisateur)
        # THEN
        # L'utilisateur est créé
        assert creation_ok
        # et il possède un identifiant
        assert utilisateur.id_utilisateur is not None

    def test_chercher_utilisateur_par_id(self):
        """Recherche par id d'un utilisateur"""
        # GIVEN
        sel = creer_sel()
        mot_de_passe_hash = hacher_mot_de_passe("abracadabra", sel)
        utilisateur = Utilisateur(
            pseudo="Pierre",
            adresse_email="pierre.martin@ensai.fr",
            mot_de_passe=mot_de_passe_hash,
            sel=sel
        )
        self.utilisateur_dao.creer(utilisateur)
        # WHEN
        utilisateur_retrouve = self.utilisateur_dao.chercher_utilisateur_par_id(utilisateur.id_utilisateur)
        # THEN
        assert utilisateur_retrouve is not None
        # Vérifie que l'utilisateur récupéré est le bon
        assert utilisateur_retrouve.pseudo == utilisateur.pseudo

    def test_chercher_utilisateur_par_pseudo(self):
        """Recherche par pseudo d'un utilisateur"""
        # GIVEN
        sel = creer_sel()
        mot_de_passe_hash = hacher_mot_de_passe("honolulu", sel)
        utilisateur = Utilisateur(
            pseudo="Alice",
            adresse_email="alice.martin@ensai.fr",
            mot_de_passe=mot_de_passe_hash,
            sel=sel
        )
        self.utilisateur_dao.creer(utilisateur)
        # WHEN
        utilisateur_retrouve = self.utilisateur_dao.chercher_utilisateur_par_pseudo(utilisateur.pseudo)
        # THEN
        assert utilisateur_retrouve is not None
        # Vérifie que l'utilisateur récupéré est le bon
        assert utilisateur_retrouve.id_utilisateur == utilisateur.id_utilisateur


if __name__ == "__main__":
    unittest.main()
