import unittest
from unittest.mock import MagicMock
from src.service.mot_de_passe_service import valider_pseudo_utilisateur_mot_de_passe, hacher_mot_de_passe, creer_sel
from src.dao.utilisateur_dao import UtilisateurDAO
from src.Model.utilisateur import Utilisateur


class TestMotDePasseService(unittest.TestCase):
    def setUp(self):
        self.utilisateur_DAO = MagicMock(spec=UtilisateurDAO)

    def test_hacher_mot_de_passe_avec_sel(self):
        """Test du hachage d'un mot de passe avec un sel fourni."""
        mot_de_passe = "monMotDePasse"
        sel = "monSelAleatoire"
        mot_de_passe_hache = hacher_mot_de_passe(mot_de_passe, sel)

        # Vérifier que le hachage est toujours le même avec le même mot de passe et le même sel
        self.assertEqual(mot_de_passe_hache, hacher_mot_de_passe(mot_de_passe, sel))

    def test_hacher_mot_de_passe_sans_sel(self):
        """Test du hachage d'un mot de passe sans fournir de sel."""
        mot_de_passe = "monMotDePasse"
        mot_de_passe_hache_1 = hacher_mot_de_passe(mot_de_passe)
        mot_de_passe_hache_2 = hacher_mot_de_passe(mot_de_passe)

        # Vérifier que le hachage est différent à chaque fois sans sel fourni
        self.assertNotEqual(mot_de_passe_hache_1, mot_de_passe_hache_2)

    def test_creer_sel(self):
        """Test de la génération d'un sel aléatoire."""
        sel_1 = creer_sel()
        sel_2 = creer_sel()

        # Vérifier que les deux sels générés sont différents
        self.assertNotEqual(sel_1, sel_2)
        # Vérifier la longueur du sel
        self.assertEqual(len(sel_1), 32)  # En hexadécimal, 16 bytes génèrent 32 caractères

    def test_authentification_reussie(self):
        """Test d'une authentification réussie avec pseudo et mot de passe corrects."""
        pseudo = "Jean"
        adresse_email = "jean@example.com"
        mot_de_passe = "motDePasseCorrect"
        sel = creer_sel()
        mot_de_passe_hache = hacher_mot_de_passe(mot_de_passe, sel)

        # Création de l'objet utilisateur avec les informations correctes
        utilisateur = Utilisateur(pseudo=pseudo, adresse_email=adresse_email, mot_de_passe=mot_de_passe_hache, sel=sel)

        # Configuration du mock pour renvoyer cet utilisateur lors de la recherche par pseudo
        self.utilisateur_DAO.chercher_utilisateur_par_pseudo.return_value = utilisateur

        # Test de la fonction
        utilisateur_retourne = valider_pseudo_utilisateur_mot_de_passe(pseudo, mot_de_passe, self.utilisateur_DAO)

        # Vérification que l'authentification est réussie
        self.assertEqual(utilisateur_retourne, utilisateur)

    def test_authentification_echouee_pseudo_incorrect(self):
        """Test d'une authentification échouée avec un pseudo incorrect."""
        pseudo = "JeanInconnu"
        mot_de_passe = "motDePasseCorrect"

        # Le mock renvoie None pour simuler un utilisateur inexistant
        self.utilisateur_DAO.chercher_utilisateur_par_pseudo.return_value = None

        # Vérification que l'exception est levée
        with self.assertRaises(Exception) as context:
            valider_pseudo_utilisateur_mot_de_passe(pseudo, mot_de_passe, self.utilisateur_DAO)
        self.assertEqual(str(context.exception), "Nom d'utilisateur incorrect")

    def test_authentification_echouee_mot_de_passe_incorrect(self):
        """Test d'une authentification échouée avec un mot de passe incorrect."""
        pseudo = "Jean"
        adresse_email = "jean@example.com"
        mot_de_passe_incorrect = "motDePasseIncorrect"
        mot_de_passe_correct = "motDePasseCorrect"
        sel = creer_sel()
        mot_de_passe_hache_correct = hacher_mot_de_passe(mot_de_passe_correct, sel)

        # Création de l'objet utilisateur avec le mot de passe correct
        utilisateur = Utilisateur(
            pseudo=pseudo, adresse_email=adresse_email, mot_de_passe=mot_de_passe_hache_correct, sel=sel
        )

        # Configuration du mock pour renvoyer cet utilisateur
        self.utilisateur_DAO.chercher_utilisateur_par_pseudo.return_value = utilisateur

        # Vérification que l'exception est levée pour un mot de passe incorrect
        with self.assertRaises(Exception) as context:
            valider_pseudo_utilisateur_mot_de_passe(pseudo, mot_de_passe_incorrect, self.utilisateur_DAO)
        self.assertEqual(str(context.exception), "Mot de passe incorrect")


if __name__ == "__main__":
    unittest.main()
