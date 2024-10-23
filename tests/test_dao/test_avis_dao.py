from unittest.mock import MagicMock, patch

import pytest

from src.business_object.avis import Avis
from src.dao.avis_dao import AvisDAO
from src.dao.utilisateur_dao import UtilisateurDAO
from src.Service.film_service import FilmService


@pytest.fixture
def setup_avis_dao():
    # GIVEN: Simuler les dépendances
    film_service = MagicMock(spec=FilmService)

    # Créer une instance de AvisDAO
    avis_dao = AvisDAO()

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
    mock_cursor.fetchone.return_value = [1]
    # Simuler que le film est trouvé dans la base

    # WHEN: Création de l'avis pour le film existant
    avis = Avis(id_avis=None, id_film=1184918, utilisateur='Soukayna', note=5,
                commentaire="Film incroyable")
    resultat = avis_dao.creer_avis(avis)

    # THEN: Vérifier que l'avis a été correctement créé
    assert resultat


def test_creer_avis_film_non_existant(setup_avis_dao):
    avis_dao, film_service, mock_cursor = setup_avis_dao

    # GIVEN: Le film n'existe pas dans la base de données
    mock_cursor.fetchone.return_value = None
    # Le film n'est pas trouvé dans la base

    # GIVEN: Simuler la création du film via le service de film
    film_service.creer_film.return_value = True
    # Simuler la création réussie du film

    # WHEN: Création de l'avis pour un film non existant
    avis = Avis(id_avis=None, id_film=1184918, utilisateur='Soukayna', note=5,
                commentaire="Film incroyable")
    resultat = avis_dao.creer_avis(avis)

    # THEN: Vérifier que l'avis a été correctement créé
    assert resultat


# Test pour un avis existant
def test_modifier_avis_existant(setup_avis_dao):
    avis_dao, _, mock_cursor = setup_avis_dao

    # GIVEN: Le film et l'avis existent dans la base de données
    mock_cursor.fetchone.side_effect = [[1], [1]]  # Le film et l'avis existent

    # WHEN: Modification de l'avis
    avis = Avis(id_avis=1, id_film=1184918, utilisateur='Soukayna', note=4,
                commentaire="Nouveau commentaire")
    resultat = avis_dao.modifier_avis(avis)

    # THEN: Vérifier que l'avis a été correctement modifié
    assert resultat


# Test pour un avis inexistant
def test_modifier_avis_inexistant(setup_avis_dao):
    avis_dao, _, mock_cursor = setup_avis_dao

    # GIVEN: Le film existe mais l'avis n'existe pas
    mock_cursor.fetchone.side_effect = [[1], None]
    # Le film existe, mais pas l'avis

    # WHEN: Tentative de modification de l'avis
    avis = Avis(id_avis=3, id_film=1184918, utilisateur='Soukayna', note=4, commentaire="Nouveau ")
    resultat = avis_dao.modifier_avis(avis)

    # THEN: Vérifier que la modification a échoué car l'avis n'existe pas
    assert resultat is False


def test_supprimer_avis_existant(setup_avis_dao):
    avis_dao, _, mock_cursor = setup_avis_dao

    # GIVEN: L'avis existe pour cet utilisateur et ce film
    mock_cursor.fetchone.return_value = [1]  # Simuler que l'avis est trouvé
    mock_cursor.rowcount = 1  # Simuler la suppression réussie

    # WHEN: Suppression de l'avis
    resultat = avis_dao.supprimer_avis(avis_id=1, utilisateur="Soukayna",
                                       id_film=1184918)

    # THEN: Vérifier que la suppression a réussi
    assert resultat


def test_supprimer_avis_inexistant(setup_avis_dao):
    avis_dao, _, mock_cursor = setup_avis_dao

    # GIVEN: L'avis n'existe pas pour cet utilisateur et ce film
    mock_cursor.fetchone.return_value = None
    # Simuler que l'avis n'est pas trouvé

    # WHEN: Tentative de suppression de l'avis
    resultat = avis_dao.supprimer_avis(avis_id=5, utilisateur="lEA",
                                       id_film=11918)

    # THEN: Vérifier que la suppression a échoué car l'avis n'existe pas
    assert resultat is False


# Test pour vérifier qu'aucun avis n'est trouvé pour un film donné
def test_aucun_avis_trouve_pour_film(setup_avis_dao):
    avis_dao, _, mock_cursor = setup_avis_dao

    # GIVEN: Aucun avis n'existe pour le film donné
    mock_cursor.fetchall.return_value = []

    # WHEN: Tentative de lecture des avis pour ce film
    resultat = avis_dao.lire_avis(id_film=111918)

    # THEN: Vérifier que la méthode retourne un message indiquant
    # qu'il n'y a pas d'avis
    assert resultat == "Aucun avis trouvé."


def test_lire_avis_par_utilisateur_pour_film(setup_avis_dao):
    avis_dao, _, mock_cursor = setup_avis_dao

    # GIVEN: Un avis existe pour cet utilisateur et ce film
    mock_cursor.fetchall.return_value = [
        {'id': 1, 'id_film': 1184918, 'utilisateur': 'Soukayna', 'note': 5, 'commentaire': "Film incroyable"}
    ]

    # WHEN: Lecture de l'avis de l'utilisateur pour ce film
    avis_list = avis_dao.lire_avis(id_film=1184918, utilisateur="Soukayna")

    # Diagnostic : vérifier la liste des avis retournée
    print(f"Liste des avis retournés : {avis_list}")

    # THEN: Vérifier que l'avis est bien celui de l'utilisateur pour le film
    assert len(avis_list) == 1
    avis = avis_list[0]
    assert avis.id_film == 1184918
    assert avis.utilisateur == 'Soukayna'
    assert avis.note == 5
    assert avis.commentaire == "Film incroyable"

    # Vérification de la requête SQL
    mock_cursor.execute.assert_called_with("SELECT * FROM avis WHERE id_film = %s AND utilisateur = %s;", (1184918, "Soukayna"))


# Test pour lire tous les avis pour un film spécifique
def test_lire_tous_avis_pour_film(setup_avis_dao):
    avis_dao, _, mock_cursor = setup_avis_dao

    # GIVEN: Plusieurs avis existent pour un film donné
    mock_cursor.fetchall.return_value = [
        {'id': 1, 'id_film': 1184, 'utilisateur': 'Soukayna', 'note': 5, 'commentaire': "Film incroyable"},
        {'id': 2, 'id_film': 1184, 'utilisateur': 'Yassine', 'note': 4, 'commentaire': "Très bon film"}
    ]

    # WHEN: Lecture de tous les avis pour ce film
    avis_list = avis_dao.lire_avis(id_film=1184)

    # THEN: Vérifier que tous les avis pour le film sont récupérés
    assert len(avis_list) == 2
    avis_1 = avis_list[0]
    avis_2 = avis_list[1]

    assert avis_1.utilisateur == 'Soukayna'
    assert avis_1.note == 5
    assert avis_1.commentaire == "Film incroyable"

    assert avis_2.utilisateur == 'Yassine'
    assert avis_2.note == 4
    assert avis_2.commentaire == "Très bon film"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
