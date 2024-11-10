import unittest
from unittest.mock import MagicMock

from src.Model.utilisateur import Utilisateur
from src.service.mot_de_passe_service import creer_sel, hacher_mot_de_passe
from src.service.utilisateur_service import UtilisateurService


class TestUtilisateurService(unittest.TestCase):
    def setUp(self):
        # Mock du DAO utilisateur
        self.mock_utilisateur_dao = MagicMock()
        # Instance du service avec le DAO mocké
        self.utilisateur_service = UtilisateurService(self.mock_utilisateur_dao)

    def test_creation_compte_succes(self):
        """Test de la création d'un compte utilisateur réussie avec des informations valides."""
        # GIVEN
        pseudo = "Jean"
        adresse_email = "jean.martin@ensai.fr"
        mot_de_passe = "MotDePasseSecurise"

        # Simulation de la création réussie dans le DAO
        self.mock_utilisateur_dao.creer.return_value = True

        # WHEN
        utilisateur = self.utilisateur_service.creation_compte(pseudo, adresse_email, mot_de_passe)

        # THEN
        self.assertIsNotNone(utilisateur)  # Vérifie que l'utilisateur a bien été créé
        self.assertEqual(utilisateur.pseudo, pseudo)
        self.assertEqual(utilisateur.adresse_email, adresse_email)
        self.assertTrue(utilisateur.mot_de_passe.startswith(hacher_mot_de_passe(mot_de_passe, utilisateur.sel)[:10]))
        self.mock_utilisateur_dao.creer.assert_called_once_with(utilisateur)

    def test_creation_compte_echec(self):
        """Test de la création d'un compte utilisateur échouée."""
        # GIVEN
        pseudo = "Jean"
        adresse_email = "jean.martin@ensai.fr"
        mot_de_passe = "MotDePasseSecurise"

        # Simulation de l'échec de création dans le DAO
        self.mock_utilisateur_dao.creer.return_value = False

        # WHEN
        utilisateur = self.utilisateur_service.creation_compte(pseudo, adresse_email, mot_de_passe)

        # THEN
        self.assertIsNone(utilisateur)  # Vérifie que l'utilisateur n'a pas été créé
        self.mock_utilisateur_dao.creer.assert_called_once()

    def test_modifier_pseudo_succes(self):
        """Test de la modification du pseudo réussie avec un utilisateur existant."""
        # GIVEN
        id_utilisateur = 1
        nouveau_pseudo = "NouveauJean"
        utilisateur_modifie = Utilisateur(
            id_utilisateur=id_utilisateur,
            pseudo=nouveau_pseudo,
            adresse_email="jean.martin@ensai.fr",
            mot_de_passe="MotDePasseHache",
            sel="SelAleatoire",
        )

        # Simuler l'existence de l'utilisateur et la modification réussie
        self.mock_utilisateur_dao.modifier_pseudo.return_value = True
        self.mock_utilisateur_dao.chercher_utilisateur_par_id.return_value = utilisateur_modifie

        # WHEN
        utilisateur_resultat = self.utilisateur_service.modifier_pseudo(id_utilisateur, nouveau_pseudo)

        # THEN
        self.assertIsNotNone(utilisateur_resultat)
        self.assertEqual(utilisateur_resultat.pseudo, nouveau_pseudo)
        self.mock_utilisateur_dao.modifier_pseudo.assert_called_once_with(id_utilisateur, nouveau_pseudo)
        self.mock_utilisateur_dao.chercher_utilisateur_par_id.assert_called_once_with(id_utilisateur)

    def test_modifier_pseudo_echec(self):
        """Test de la modification du pseudo échouée avec un utilisateur inexistant."""
        # GIVEN
        id_utilisateur = 1
        nouveau_pseudo = "NouveauJean"

        # Simuler l’échec de la modification du pseudo
        self.mock_utilisateur_dao.modifier_pseudo.return_value = False

        # WHEN
        utilisateur_resultat = self.utilisateur_service.modifier_pseudo(id_utilisateur, nouveau_pseudo)

        # THEN
        self.assertIsNone(utilisateur_resultat)
        self.mock_utilisateur_dao.modifier_pseudo.assert_called_once_with(id_utilisateur, nouveau_pseudo)

    def test_modifier_adresse_email_succes(self):
        """Test de la modification de l'adresse e-mail réussie avec un utilisateur existant."""
        # GIVEN
        id_utilisateur = 1
        nouvelle_adresse_email = "nouveau.jean@ensai.fr"
        utilisateur_modifie = Utilisateur(
            id_utilisateur=id_utilisateur,
            pseudo="Jean",
            adresse_email=nouvelle_adresse_email,
            mot_de_passe="MotDePasseHache",
            sel="SelAleatoire",
        )

        # Simuler l'existence de l'utilisateur et la modification réussie
        self.mock_utilisateur_dao.modifier_adresse_email.return_value = True
        self.mock_utilisateur_dao.chercher_utilisateur_par_id.return_value = utilisateur_modifie

        # WHEN
        utilisateur_resultat = self.utilisateur_service.modifier_adresse_email(id_utilisateur, nouvelle_adresse_email)

        # THEN
        self.assertIsNotNone(utilisateur_resultat)
        self.assertEqual(utilisateur_resultat.adresse_email, nouvelle_adresse_email)
        self.mock_utilisateur_dao.modifier_adresse_email.assert_called_once_with(id_utilisateur, nouvelle_adresse_email)
        self.mock_utilisateur_dao.chercher_utilisateur_par_id.assert_called_once_with(id_utilisateur)

    def test_modifier_adresse_email_echec(self):
        """Test de la modification de l'adresse e-mail échouée avec un utilisateur inexistant."""
        # GIVEN
        id_utilisateur = 1
        nouvelle_adresse_email = "nouveau.jean@ensai.fr"

        # Simuler l’échec de la modification de l'adresse e-mail
        self.mock_utilisateur_dao.modifier_adresse_email.return_value = False

        # WHEN
        utilisateur_resultat = self.utilisateur_service.modifier_adresse_email(id_utilisateur, nouvelle_adresse_email)

        # THEN
        self.assertIsNone(utilisateur_resultat)
        self.mock_utilisateur_dao.modifier_adresse_email.assert_called_once_with(id_utilisateur, nouvelle_adresse_email)

    def test_modifier_mot_de_passe_succes(self):
        """Test de la modification réussie du mot de passe avec un mot de passe valide."""
        # GIVEN
        id_utilisateur = 1
        nouveau_mot_de_passe = "NouveauMotDePasseSecurise"
        sel = "SelExistant"  # Sel déjà stocké pour cet utilisateur
        utilisateur = Utilisateur(
            id_utilisateur=id_utilisateur,
            pseudo="UtilisateurTest",
            adresse_email="utilisateur.test@exemple.com",
            mot_de_passe=hacher_mot_de_passe(nouveau_mot_de_passe, sel),
            sel=sel,
        )

        # Simuler l'existence de l'utilisateur et la modification réussie
        self.mock_utilisateur_dao.chercher_utilisateur_par_id.return_value = utilisateur
        self.mock_utilisateur_dao.modifier_mot_de_passe.return_value = True

        # WHEN
        utilisateur_modifie = self.utilisateur_service.modifier_mot_de_passe(id_utilisateur, nouveau_mot_de_passe)

        # THEN
        self.assertIsNotNone(utilisateur_modifie)
        mot_de_passe_hache_attendu = hacher_mot_de_passe(nouveau_mot_de_passe, utilisateur.sel)
        self.assertEqual(utilisateur_modifie.mot_de_passe, mot_de_passe_hache_attendu)
        self.assertEqual(self.mock_utilisateur_dao.chercher_utilisateur_par_id.call_count, 2)
        self.mock_utilisateur_dao.modifier_mot_de_passe.assert_called_once_with(
            id_utilisateur, mot_de_passe_hache_attendu
        )

    def test_modifier_mot_de_passe_echec_robustesse(self):
        """Test de l'échec de la modification du mot de passe en raison d'un mot de passe trop faible."""
        # GIVEN
        id_utilisateur = 1
        mot_de_passe_faible = "12345"  # Mot de passe trop court

        # WHEN / THEN
        with self.assertRaises(Exception) as context:
            self.utilisateur_service.modifier_mot_de_passe(id_utilisateur, mot_de_passe_faible)
        self.assertIn("Le mot de passe doit contenir au moins 8 caractères", str(context.exception))


if __name__ == "__main__":
    unittest.main()
