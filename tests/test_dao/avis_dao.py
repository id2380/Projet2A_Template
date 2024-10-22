import pytest
from unittest.mock import MagicMock, patch
from src.dao.avis_dao import AvisDAO
from src.business_object.avis import Avis
from src.Service.film_service import FilmService
from src.dao.utilisateur_dao import UtilisateurDAO


@pytest.fixture
def setup_avis_dao():
    # GIVEN: Simuler les dépendances
    film_service = MagicMock(spec=FilmService)
    utilisateur_dao = MagicMock(spec=UtilisateurDAO)

    # Créer une instance de AvisDAO
    avis_dao = AvisDAO(film_service=film_service, utilisateur_dao=utilisateur_dao)

    # Simuler la connexion DB et le curseur
    connection_patch = patch('src.data.db_connection.DBConnection.connection')
    mock_connection = connection_patch.start()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    yield avis_dao, film_service, mock_cursor

    connection_patch.stop()


def test_creer_avis_film_existant(setup_avis_dao):
    avis_dao, _, mock_cursor = setup_avis_dao

    # GIVEN: Le film existe déjà dans la base de données
    mock_cursor.fetchone.return_value = [1]  # Simuler que le film est trouvé dans la base

    # WHEN: Création de l'avis pour le film existant
    avis = Avis(id_avis=None, id_film=1184918, utilisateur='Soukayna', note=5, commentaire="Film incroyable")
    resultat = avis_dao.creer_avis(avis)

    # THEN: Vérifier que l'avis a été correctement créé
    assert resultat


def test_creer_avis_film_non_existant(setup_avis_dao):
    avis_dao, film_service, mock_cursor = setup_avis_dao

    # GIVEN: Le film n'existe pas dans la base de données
    mock_cursor.fetchone.return_value = None  # Le film n'est pas trouvé dans la base

    # GIVEN: Simuler la création du film via le service de film
    film_service.creer_film.return_value = True  # Simuler la création réussie du film

    # WHEN: Création de l'avis pour un film non existant
    avis = Avis(id_avis=None, id_film=1184918, utilisateur='Soukayna', note=5, commentaire="Film incroyable")
    resultat = avis_dao.creer_avis(avis)

    # THEN: Vérifier que l'avis a été correctement créé
    assert resultat

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
