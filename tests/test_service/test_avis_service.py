from unittest import mock
from unittest.mock import MagicMock

from src.business_object.avis import Avis
from src.dao.avis_dao import AvisDAO
from src.Model.utilisateur import Utilisateur
from src.Service.avis_service import AvisService


class TestAvisService:

    @mock.patch('src.dao.avis_dao.AvisDAO.creer_avis')
    def test_ajouter_avis_success(self, mock_creer_avis):
        # GIVEN
        mock_creer_avis.return_value = True
        avis_service = AvisService(AvisDAO())

        utilisateur = Utilisateur(pseudo="Soukayna", adresse_email="soukayna@example.com", mot_de_passe="pass")

        # WHEN
        avis = avis_service.ajouter_avis(id_film=1184918, utilisateur=utilisateur, commentaire="Film incroyable", note=5)

        # THEN
        assert avis is not None

    @mock.patch('src.dao.avis_dao.AvisDAO.creer_avis')
    def test_ajouter_avis_failure(self, mock_creer_avis):
        # GIVEN
        mock_creer_avis.return_value = False
        avis_service = AvisService(AvisDAO())

        utilisateur = Utilisateur(pseudo="Soukayna", adresse_email="soukayna@example.com", mot_de_passe="pass")

        # WHEN
        avis = avis_service.ajouter_avis(id_film=1184918, utilisateur=utilisateur, commentaire="Film incroyable", note=5)

        # THEN
        assert avis is None

    @mock.patch('src.dao.avis_dao.AvisDAO.lire_avis')
    def test_obtenir_avis_par_film(self, mock_lire_avis):
        # GIVEN
        mock_lire_avis.return_value = [
            Avis(id_avis=1, id_film=1184918, utilisateur="Soukayna", note=5, commentaire="Film incroyable"),
            Avis(id_avis=2, id_film=1184918, utilisateur="Yassine", note=4, commentaire="Bon film")
        ]
        avis_service = AvisService(AvisDAO())

        # WHEN
        avis_list = avis_service.obtenir_avis_par_film(id_film=1184918)

        # THEN
        assert len(avis_list) == 2

    @mock.patch('src.dao.avis_dao.AvisDAO.lire_avis')
    def test_obtenir_avis_par_utilisateur(self, mock_lire_avis):
        # GIVEN
        mock_lire_avis.return_value = [
            Avis(id_avis=1, id_film=1184918, utilisateur="Soukayna", note=5, commentaire="Film incroyable")
        ]
        avis_service = AvisService(AvisDAO())
        utilisateur = Utilisateur(pseudo="Soukayna", adresse_email="soukayna@example.com", mot_de_passe="pass")

        # WHEN
        avis_list = avis_service.obtenir_avis_par_utilisateur(utilisateur=utilisateur)

        # THEN
        assert len(avis_list) == 1

    @mock.patch('src.dao.avis_dao.AvisDAO.modifier_avis')
    def test_modifier_avis_success(self, mock_modifier_avis):
        # GIVEN
        mock_modifier_avis.return_value = True
        avis_service = AvisService(AvisDAO())

        # WHEN
        avis = Avis(id_avis=1, id_film=1184918, utilisateur="Soukayna", note=4, commentaire="Très bon film")
        resultat = avis_service.modifier_avis(id_avis=1, utilisateur="Soukayna", id_film=1184918, commentaire="Très bon film", note=4)

        # THEN
        assert resultat

    @mock.patch('src.dao.avis_dao.AvisDAO.modifier_avis')
    def test_modifier_avis_failure(self, mock_modifier_avis):
        # GIVEN
        mock_modifier_avis.return_value = False
        avis_service = AvisService(AvisDAO())

        # WHEN
        resultat = avis_service.modifier_avis(id_avis=1, utilisateur="Soukayna", id_film=1184918, commentaire="Très bon film", note=4)

        # THEN
        assert not resultat

    @mock.patch('src.dao.avis_dao.AvisDAO.supprimer_avis')
    def test_supprimer_avis_success(self, mock_supprimer_avis):
        # GIVEN
        mock_supprimer_avis.return_value = True
        avis_service = AvisService(AvisDAO())

        # WHEN
        resultat = avis_service.supprimer_avis(avis_id=1, utilisateur="Soukayna", id_film=1184918)

        # THEN
        assert resultat

    @mock.patch('src.dao.avis_dao.AvisDAO.supprimer_avis')
    def test_supprimer_avis_failure(self, mock_supprimer_avis):
        # GIVEN
        mock_supprimer_avis.return_value = False
        avis_service = AvisService(AvisDAO())

        # WHEN
        resultat = avis_service.supprimer_avis(avis_id=1, utilisateur="Soukayna", id_film=1184918)

        # THEN
        assert not resultat

    @mock.patch('src.dao.avis_dao.AvisDAO.lire_avis')
    def test_calculer_note_moyenne(self, mock_lire_avis):
        # GIVEN
        mock_lire_avis.return_value = [
            Avis(id_avis=1, id_film=1184918, utilisateur="Soukayna", note=5, commentaire="Film incroyable"),
            Avis(id_avis=2, id_film=1184918, utilisateur="Yassine", note=4, commentaire="Bon film")
        ]
        avis_service = AvisService(AvisDAO())

        # WHEN
        note_moyenne = avis_service.calculer_note_moyenne(id_film=1184918)

        # THEN
        assert note_moyenne == 4.5

    @mock.patch('src.dao.avis_dao.AvisDAO.lire_avis')
    def test_calculer_note_moyenne_sans_avis(self, mock_lire_avis):
        # GIVEN
        mock_lire_avis.return_value = "Aucun avis trouvé."
        avis_service = AvisService(AvisDAO())

        # WHEN
        note_moyenne = avis_service.calculer_note_moyenne(id_film=1184918)

        # THEN
        assert note_moyenne == 0.0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
