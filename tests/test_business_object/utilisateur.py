import unittest

from src.business_object.Utilisateur import \
    Utilisateur  # Ajustez cet import selon la structure réelle de votre module


class TestUtilisateur(unittest.TestCase):
    def setUp(self):
        # Initialisation d'une instance de Utilisateur avec mot de passe haché
        self.utilisateur = Utilisateur(id_utilisateur=1, pseudo="johndoe", email="john@example.com", mot_de_passe="securepassword")

    def test_mot_de_passe_non_accessible_directement(self):
        """Teste que l'accès direct au mot de passe soulève une AttributeError."""
        with self.assertRaises(AttributeError):
            print(self.utilisateur.mot_de_passe)

    def test_verification_mot_de_passe_correcte(self):
        """Teste que le bon mot de passe est vérifié avec succès."""
        self.assertTrue(self.utilisateur.verifier_mot_de_passe("securepassword"))

    def test_verification_mot_de_passe_incorrecte(self):
        """Teste qu'un mot de passe incorrect n'est pas vérifié."""
        self.assertFalse(self.utilisateur.verifier_mot_de_passe("wrongpassword"))

    def test_changement_mot_de_passe(self):
        """Teste le changement de mot de passe et sa vérification."""
        self.utilisateur.mot_de_passe = "newsecurepassword"
        self.assertTrue(self.utilisateur.verifier_mot_de_passe("newsecurepassword"))
        self.assertFalse(self.utilisateur.verifier_mot_de_passe("securepassword"))

if __name__ == '__main__':
    unittest.main()
