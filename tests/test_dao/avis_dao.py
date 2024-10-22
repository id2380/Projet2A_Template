import unittest
from unittest.mock import MagicMock, patch

from src.business_object.avis import Avis
from src.business_object.utilisateur import Utilisateur
from src.dao.avis_dao import AvisDAO
from src.dao.utilisateur_dao import UtilisateurDAO
from src.service.film_service import FilmService


class TestAvisDAO(unittest.TestCase):

    def setUp(self):
        """Configuration des mocks avant chaque test"""
        # Mock pour FilmService
        self.film_service_mock = MagicMock(spec=FilmService)

        # Mock pour UtilisateurDAO
        self.utilisateur_dao_mock = MagicMock(spec=UtilisateurDAO)

        # Initialisation de AvisDAO avec les mocks
        self.avis_dao = AvisDAO(self.film_service_mock, self.utilisateur_dao_mock)

        # Création de l'utilisateur de test
        self.utilisateur = Utilisateur(
            pseudo="Soukayna",
            adresse_email="soukayna@example.com",
            mot_de_passe="securepassword"
        )
        self.utilisateur.id_utilisateur = 1

    @patch('src.data.db_connection.DBConnection')
    def test_creer_avis_film_existant(self, db_connection_mock):
        """Test de la création d'un avis pour un film existant"""

        # GIVEN
        avis = Avis(
            id_film=123,  # ID du film existant
            utilisateur="Soukayna",
            note=5,
            commentaire="Film incroyable"
        )

        # Simulation de la base de données renvoyant un film existant
        db_cursor_mock = MagicMock()
        db_cursor_mock.fetchone.return_value = [123]  # Simule que le film existe
        db_connection_mock().connection.cursor.return_value.__enter__.return_value = db_cursor_mock

        # Simulation de la méthode utilisateur_dao
        self.utilisateur_dao_mock.read_utilisateur_by_pseudo.return_value = self.utilisateur

        # WHEN
        result = self.avis_dao.creer_avis(avis)

        # THEN
        self.assertTrue(res5ult, "L'avis n'a pas été créé correctement")
        db_cursor_mock.execute.assert_called_with("SELECT id_film FROM film WHERE id_film = %s;", (123,))
        db_cursor_mock.execute.assert_any_call(
            """
            INSERT INTO avis(id_film, utilisateur, note, commentaire, id_utilisateur)
            VALUES (%(id_film)s, %(utilisateur)s, %(note)s, %(commentaire)s, %(id_utilisateur)s)
            RETURNING id;
            """,
            {
                "id_film": 123,
                "utilisateur": "Soukayna",
                "note": 5,
                "commentaire": "Film incroyable",
                "id_utilisateur": 1
            }
        )

    @patch('src.data.db_connection.DBConnection')
    def test_creer_avis_film_inexistant(self, db_connection_mock):
        """Test de la création d'un avis pour un film inexistant, où le film est créé via l'API TMDB"""

        # GIVEN
        avis = Avis(
            id_film=456,  # ID du film inexistant
            utilisateur="Soukayna",
            note=4,
            commentaire="Super film"
        )

        # Simulation de la base de données ne trouvant pas le film
        db_cursor_mock = MagicMock()
        db_cursor_mock.fetchone.side_effect = [None, 456]  # Simule que le film n'existe pas puis est créé
        db_connection_mock().connection.cursor.return_value.__enter__.return_value = db_cursor_mock

        # Simulation de l'API TMDB créant un nouveau film
        film_mock = MagicMock()
        film_mock.id_film = 456
        self.film_service_mock.creer_film_par_id_tmdb.return_value = film_mock

        # Simulation de la méthode utilisateur_dao
        self.utilisateur_dao_mock.read_utilisateur_by_pseudo.return_value = self.utilisateur

        # WHEN
        result = self.avis_dao.creer_avis(avis)

        # THEN
        self.assertTrue(result, "L'avis n'a pas été créé correctement pour le film inexistant")
        self.film_service_mock.creer_film_par_id_tmdb.assert_called_once_with(456)
        db_cursor_mock.execute.assert_called_with("SELECT id_film FROM film WHERE id_film = %s;", (456,))
        db_cursor_mock.execute.assert_any_call(
            """
            INSERT INTO avis(id_film, utilisateur, note, commentaire, id_utilisateur)
            VALUES (%(id_film)s, %(utilisateur)s, %(note)s, %(commentaire)s, %(id_utilisateur)s)
            RETURNING id;
            """,
            {
                "id_film": 456,
                "utilisateur": "Soukayna",
                "note": 4,
                "commentaire": "Super film",
                "id_utilisateur": 1
            }
        )


if __name__ == '__main__':
    unittest.main()
