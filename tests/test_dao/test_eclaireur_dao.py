import unittest
from unittest.mock import MagicMock, patch

from src.business_object.utilisateur import Utilisateur
from src.dao.eclaireur_dao import EclaireurDAO
from src.dao.utilisateur_dao import UtilisateurDAO
from src.Service.utilisateur_service import UtilisateurService


class TestAjouterEclaireur(unittest.TestCase):
    def test_ajouter_eclaireur_utilisateur_existant(self, mock_db_connection):
        #créer un vrai utilisateur
        gab_utilisateur = Utilisateur(pseudo = "gob", adresse_email = "gab@gab.fr", mot_de_passe = "mdp")
        tib_eclaireur = Utilisateur(pseudo = "tob", adresse_email = "tib@tib.fr", mot_de_passe = "mdp")
        utilisateur_dao = UtilisateurDAO()
        utilisateur_dao.creer(tib_eclaireur)
        utilisateur_dao.creer(gab_utilisateur)
        

        #
        assert True


    @patch('db_connection.DBConnection')
    def test_ajouter_eclaireur_utilisateur_non_existant(self, mock_db_connection):
        # Configurer le mock pour simuler aucun utilisateur trouvé
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None  # Aucun id_utilisateur trouvé
        mock_db_connection.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        
        # Créer une instance de votre classe
        instance = YourClass()
        
        # Appeler la méthode
        result = instance.ajouter_eclaireur("pseudo_inexistant")
        
        # Vérifier les résultats
        self.assertFalse(result)
        mock_cursor.execute.assert_called_once()  # Assurez-vous que la première requête a été exécutée

    @patch('db_connection.DBConnection')
    def test_ajouter_eclaireur_erreur_insertion(self, mock_db_connection):
        # Configurer le mock pour simuler un utilisateur trouvé
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [(1,)]  # id_utilisateur trouvé
        mock_db_connection.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        
        # Simuler une erreur lors de l'insertion
        mock_cursor.execute.side_effect = [None, Exception("Erreur d'insertion")]

        # Créer une instance de votre classe
        instance = YourClass()
        
        # Appeler la méthode
        result = instance.ajouter_eclaireur("pseudo_utilisateur")
        
        # Vérifier les résultats
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
