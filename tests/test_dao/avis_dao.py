from unittest.mock import MagicMock, patch

import pytest

from src.business_object.Avis import Avis
from src.dao.avis_dao import AvisDAO
from src.dao.utilisateur_dao import UtilisateurDAO
from src.Service.film_service import FilmService


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


# Test pour un avis existant
def test_modifier_avis_existant(setup_avis_dao):
    avis_dao, _, mock_cursor = setup_avis_dao

    # GIVEN: Le film et l'avis existent dans la base de données
    mock_cursor.fetchone.side_effect = [[1], [1]]  # Le film et l'avis existent

    # WHEN: Modification de l'avis
    avis = Avis(id_avis=1, id_film=1184918, utilisateur='Soukayna', note=4, commentaire="Nouveau commentaire")
    resultat = avis_dao.modifier_avis(avis)

    # THEN: Vérifier que l'avis a été correctement modifié
    assert resultat

    # THEN: Vérifier que la requête SQL de modification a été appelée
    mock_cursor.execute.assert_called_with(
        """
        UPDATE avis
        SET note = %(note)s, commentaire = %(commentaire)s
        WHERE id_film = %(id_film)s AND utilisateur = %(utilisateur)s;
        """,
        {
            "id_film": avis.id_film,
            "utilisateur": avis.utilisateur,
            "note": avis.note,
            "commentaire": avis.commentaire
        }
    )


# Test pour un avis inexistant
def test_modifier_avis_inexistant(setup_avis_dao):
    avis_dao, _, mock_cursor = setup_avis_dao

    # GIVEN: Le film existe mais l'avis n'existe pas
    mock_cursor.fetchone.side_effect = [[1], None]  # Le film existe, mais pas l'avis

    # WHEN: Tentative de modification de l'avis
    avis = Avis(id_avis=1, id_film=1184918, utilisateur='Soukayna', note=4, commentaire="Nouveau commentaire")
    resultat = avis_dao.modifier_avis(avis)

    # THEN: Vérifier que la modification a échoué car l'avis n'existe pas
    assert not resultat

    # THEN: Vérifier que la requête de modification n'a pas été appelée
    mock_cursor.execute.assert_not_called()

def test_supprimer_avis_existant(setup_avis_dao):
    avis_dao, _, mock_cursor = setup_avis_dao

    # GIVEN: L'avis existe pour cet utilisateur et ce film
    mock_cursor.fetchone.return_value = [1]  # Simuler que l'avis est trouvé
    mock_cursor.rowcount = 1  # Simuler la suppression réussie

    # WHEN: Suppression de l'avis
    resultat = avis_dao.supprimer_avis(avis_id=1, utilisateur="Soukayna", id_film=1184918)

    # THEN: Vérifier que la suppression a réussi
    assert resultat

    # THEN: Vérifier que la requête de suppression a été appelée
    mock_cursor.execute.assert_called_with(
        "DELETE FROM avis WHERE id = %(id)s AND utilisateur = %(utilisateur)s AND id_film = %(id_film)s;",
        {"id": 1, "utilisateur": "Soukayna", "id_film": 1184918}
    )


def test_supprimer_avis_inexistant(setup_avis_dao):
    avis_dao, _, mock_cursor = setup_avis_dao

    # GIVEN: L'avis n'existe pas pour cet utilisateur et ce film
    mock_cursor.fetchone.return_value = None  # Simuler que l'avis n'est pas trouvé

    # WHEN: Tentative de suppression de l'avis
    resultat = avis_dao.supprimer_avis(avis_id=1, utilisateur="Soukayna", id_film=1184918)

    # THEN: Vérifier que la suppression a échoué car l'avis n'existe pas
    assert not resultat

    # THEN: Vérifier que la requête de suppression n'a pas été appelée
    mock_cursor.execute.assert_not_called()

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
