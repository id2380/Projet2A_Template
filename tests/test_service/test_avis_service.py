from unittest import mock
from unittest.mock import MagicMock
from src.business_object.avis import Avis
from src.dao.avis_dao import AvisDAO
from src.service.avis_service import AvisService
from src.Model.utilisateur import Utilisateur


class TestAvisService:

    @mock.patch('src.dao.avis_dao.AvisDAO.creer_avis')
    def test_ajouter_avis_success(self, mock_creer_avis):
        # GIVEN
        mock_creer_avis.return_value = True
        avis_service = AvisService()
        utilisateur = Utilisateur(pseudo="Soukayna", adresse_email="soukayna@example.com", mot_de_passe="pass")

        # WHEN
        avis = avis_service.ajouter_avis(id_film=1184918, utilisateur="Soukayna", commentaire="Film incroyable", note=5)

        # THEN
        assert avis is not None
        assert avis.id_film == 1184918
        assert avis.utilisateur == "Soukayna"
        assert avis.commentaire == "Film incroyable"
        assert avis.note == 5

    @mock.patch('src.dao.avis_dao.AvisDAO.creer_avis')
    def test_ajouter_avis_failure(self, mock_creer_avis):
        # GIVEN
        mock_creer_avis.return_value = False
        avis_service = AvisService()
        utilisateur = Utilisateur(pseudo="Soukayna", adresse_email="soukayna@example.com", mot_de_passe="pass")

        # WHEN
        avis = avis_service.ajouter_avis(id_film=1184918, utilisateur="Soukayna", commentaire="Film incroyable", note=5)

        # THEN
        assert avis is None

    @mock.patch('src.dao.avis_dao.AvisDAO.lire_avis')
    def test_obtenir_avis_par_film(self, mock_lire_avis):
        # GIVEN
        mock_lire_avis.return_value = [
            Avis(id_avis=1, id_film=1184918, utilisateur="Soukayna", note=5, commentaire="Film incroyable"),
            Avis(id_avis=2, id_film=1184918, utilisateur="Yassine", note=4, commentaire="Bon film")
        ]
        avis_service = AvisService()

        # WHEN
        avis_list = avis_service.obtenir_avis_par_film(id_film=1184918)

        # THEN
        assert len(avis_list) == 2
        assert avis_list[0].utilisateur == "Soukayna"
        assert avis_list[1].utilisateur == "Yassine"

    @mock.patch('src.dao.avis_dao.AvisDAO.lire_avis')
    def test_obtenir_avis_par_utilisateur(self, mock_lire_avis):
        # GIVEN
        mock_lire_avis.return_value = [
            Avis(id_avis=1, id_film=1184918, utilisateur="Soukayna", note=5, commentaire="Film incroyable")
        ]
        avis_service = AvisService()

        # WHEN
        avis_list = avis_service.obtenir_avis_par_utilisateur(utilisateur_pseudo="Soukayna")

        # THEN
        assert len(avis_list) == 1
        assert avis_list[0].utilisateur == "Soukayna"

    @mock.patch('src.dao.avis_dao.AvisDAO.modifier_avis')
    def test_modifier_avis_success(self, mock_modifier_avis):
        # GIVEN
        mock_modifier_avis.return_value = True
        avis_service = AvisService()

        # WHEN
        resultat = avis_service.modifier_avis(id_film=1184918, utilisateur="Soukayna", commentaire="Très bon film", note=4)

        # THEN
        assert resultat is True

    @mock.patch('src.dao.avis_dao.AvisDAO.modifier_avis')
    def test_modifier_avis_failure(self, mock_modifier_avis):
        # GIVEN
        mock_modifier_avis.return_value = False
        avis_service = AvisService()

        # WHEN
        resultat = avis_service.modifier_avis(id_film=1184918, utilisateur="Soukayna", commentaire="Très bon film", note=4)

        # THEN
        assert resultat is False

    @mock.patch('src.dao.avis_dao.AvisDAO.supprimer_avis')
    def test_supprimer_avis_success(self, mock_supprimer_avis):
        # GIVEN
        mock_supprimer_avis.return_value = True
        avis_service = AvisService()

        # WHEN
        resultat = avis_service.supprimer_avis(id_film=1184918, utilisateur_pseudo="Soukayna")

        # THEN
        assert resultat is True

    @mock.patch('src.dao.avis_dao.AvisDAO.supprimer_avis')
    def test_supprimer_avis_failure(self, mock_supprimer_avis):
        # GIVEN
        mock_supprimer_avis.return_value = False
        avis_service = AvisService()

        # WHEN
        resultat = avis_service.supprimer_avis(id_film=1184918, utilisateur_pseudo="Soukayna")

        # THEN
        assert resultat is False

    @mock.patch('src.dao.avis_dao.AvisDAO.lire_avis')
    def test_calculer_note_moyenne(self, mock_lire_avis):
        # GIVEN
        mock_lire_avis.return_value = [
            Avis(id_avis=1, id_film=1184918, utilisateur="Soukayna", note=5, commentaire="Film incroyable"),
            Avis(id_avis=2, id_film=1184918, utilisateur="Yassine", note=4, commentaire="Bon film")
        ]
        avis_service = AvisService()

        # WHEN
        note_moyenne = avis_service.calculer_note_moyenne(id_film=1184918)

        # THEN
        assert note_moyenne == 4.5

    @mock.patch('src.dao.avis_dao.AvisDAO.lire_avis')
    def test_calculer_note_moyenne_sans_avis(self, mock_lire_avis):
        # GIVEN
        mock_lire_avis.return_value = "Aucun avis trouvé."
        avis_service = AvisService()

        # WHEN
        note_moyenne = avis_service.calculer_note_moyenne(id_film=1184918)

        # THEN
        assert note_moyenne == 0.0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
