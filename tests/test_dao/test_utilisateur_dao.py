import unittest

from src.dao.utilisateur_dao import UtilisateurDAO
from src.data.db_connection import DBConnection
from src.Model.utilisateur import Utilisateur
from src.service.mot_de_passe_service import creer_sel, hacher_mot_de_passe


class TestUtilisateurDAO(unittest.TestCase):
    def setUp(self):
        # Initialisation du DAO et de la liste pour stocker les utilisateurs créés
        self.utilisateur_dao = UtilisateurDAO()
        self.id_utilisateurs_crees = []

    def tearDown(self):
        # Nettoyage : suppression des utilisateurs créés après chaque test
        if self.id_utilisateurs_crees:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    for id_utilisateur in self.id_utilisateurs_crees:
                        cursor.execute(
                            "DELETE FROM utilisateur WHERE id_utilisateur = %s;",
                            (id_utilisateur,),
                        )
                connection.commit()
            self.id_utilisateurs_crees = (
                []
            )  # Réinitialise la liste après la suppression

    def test_creer(self):
        """Test de création d'un utilisateur"""
        # GIVEN
        sel = creer_sel()
        mot_de_passe_hash = hacher_mot_de_passe("blablabla", sel)
        utilisateur = Utilisateur(
            pseudo="Jean",
            adresse_email="jean.martin@ensai.fr",
            mot_de_passe=mot_de_passe_hash,
            sel=sel,
        )

        # WHEN
        creation_ok = self.utilisateur_dao.creer(utilisateur)
        # Enregistrer l'ID pour suppression après le test
        self.id_utilisateurs_crees.append(utilisateur.id_utilisateur)

        # THEN
        self.assertTrue(creation_ok, "La création de l'utilisateur a échoué.")
        self.assertIsNotNone(
            utilisateur.id_utilisateur,
            "L'ID de l'utilisateur n'a pas été assigné après la création.",
        )

    def test_chercher_utilisateur_par_id(self):
        """Recherche par id d'un utilisateur"""
        # GIVEN
        sel = creer_sel()
        mot_de_passe_hash = hacher_mot_de_passe("abracadabra", sel)
        utilisateur = Utilisateur(
            pseudo="Pierre",
            adresse_email="pierre.martin@ensai.fr",
            mot_de_passe=mot_de_passe_hash,
            sel=sel,
        )
        self.utilisateur_dao.creer(utilisateur)
        # Enregistrer l'ID pour suppression après le test
        self.id_utilisateurs_crees.append(utilisateur.id_utilisateur)

        # WHEN
        utilisateur_retrouve = (
            self.utilisateur_dao.chercher_utilisateur_par_id(
                utilisateur.id_utilisateur
            )
        )

        # THEN
        self.assertIsNotNone(
            utilisateur_retrouve, "L'utilisateur n'a pas été trouvé par ID."
        )
        self.assertEqual(
            utilisateur_retrouve.pseudo,
            utilisateur.pseudo,
            "Le pseudo de l'utilisateur trouvé ne correspond pas.",
        )

    def test_chercher_utilisateur_par_pseudo(self):
        """Recherche par pseudo d'un utilisateur"""
        # GIVEN
        sel = creer_sel()
        mot_de_passe_hash = hacher_mot_de_passe("honolulu", sel)
        utilisateur = Utilisateur(
            pseudo="Alice",
            adresse_email="alice.martin@ensai.fr",
            mot_de_passe=mot_de_passe_hash,
            sel=sel,
        )
        self.utilisateur_dao.creer(utilisateur)
        # Enregistrer l'ID pour suppression après le test
        self.id_utilisateurs_crees.append(utilisateur.id_utilisateur)

        # WHEN
        utilisateur_retrouve = (
            self.utilisateur_dao.chercher_utilisateur_par_pseudo(
                utilisateur.pseudo
            )
        )

        # THEN
        self.assertIsNotNone(
            utilisateur_retrouve, "L'utilisateur n'a pas été trouvé par ID."
        )
        self.assertEqual(
            utilisateur_retrouve.id_utilisateur,
            utilisateur.id_utilisateur,
            "L'identifiant de l'utilisateur trouvé ne correspond pas.",
        )

    def test_modifier_pseudo(self):
        """Test de la modification du pseudo d'un utilisateur."""
        # GIVEN
        sel = creer_sel()
        mot_de_passe_hash = hacher_mot_de_passe("MotDePasseInitial", sel)
        utilisateur = Utilisateur(
            pseudo="VieuxPseudo",
            adresse_email="vieux.pseudo@exemple.com",
            mot_de_passe=mot_de_passe_hash,
            sel=sel,
        )
        self.utilisateur_dao.creer(utilisateur)
        # Enregistrer l'ID pour suppression après le test
        self.id_utilisateurs_crees.append(utilisateur.id_utilisateur)
        nouveau_pseudo = "NouveauPseudo"

        # WHEN
        modification_ok = self.utilisateur_dao.modifier_pseudo(
            utilisateur.id_utilisateur, nouveau_pseudo
        )
        utilisateur_modifie = self.utilisateur_dao.chercher_utilisateur_par_id(
            utilisateur.id_utilisateur
        )

        # THEN
        self.assertTrue(modification_ok, "La modification du pseudo a échoué.")
        self.assertEqual(
            utilisateur_modifie.pseudo,
            nouveau_pseudo,
            "Le pseudo n'a pas été correctement modifié.",
        )

    def test_modifier_adresse_email(self):
        """Test de la modification de l'adresse email d'un utilisateur."""
        # GIVEN
        sel = creer_sel()
        mot_de_passe_hash = hacher_mot_de_passe("MotDePasseInitial", sel)
        utilisateur = Utilisateur(
            pseudo="EmailTest",
            adresse_email="vieuxemail@example.com",
            mot_de_passe=mot_de_passe_hash,
            sel=sel,
        )
        self.utilisateur_dao.creer(utilisateur)
        # Enregistrer l'ID pour suppression après le test
        self.id_utilisateurs_crees.append(utilisateur.id_utilisateur)
        nouvelle_adresse_email = "nouvelemail@exemple.com"

        # WHEN
        modification_ok = self.utilisateur_dao.modifier_adresse_email(
            utilisateur.id_utilisateur, nouvelle_adresse_email
        )
        utilisateur_modifie = self.utilisateur_dao.chercher_utilisateur_par_id(
            utilisateur.id_utilisateur
        )

        # THEN
        self.assertTrue(
            modification_ok, "La modification de l'adresse email a échoué."
        )
        self.assertEqual(
            utilisateur_modifie.adresse_email,
            nouvelle_adresse_email,
            "L'adresse email n'a pas été correctement modifiée.",
        )

    def test_modifier_mot_de_passe(self):
        """Test de la modification du mot de passe d'un utilisateur."""
        # GIVEN
        sel = creer_sel()
        mot_de_passe_hash = hacher_mot_de_passe("MotDePasseInitial", sel)
        utilisateur = Utilisateur(
            pseudo="MotDePasseTest",
            adresse_email="motdepassetest@exemple.com",
            mot_de_passe=mot_de_passe_hash,
            sel=sel,
        )
        self.utilisateur_dao.creer(utilisateur)
        # Enregistrer l'ID pour suppression après le test
        self.id_utilisateurs_crees.append(utilisateur.id_utilisateur)
        nouveau_mot_de_passe = hacher_mot_de_passe("NouveauMotDePasse", sel)

        # WHEN
        modification_ok = self.utilisateur_dao.modifier_mot_de_passe(
            utilisateur.id_utilisateur, nouveau_mot_de_passe
        )
        utilisateur_modifie = self.utilisateur_dao.chercher_utilisateur_par_id(
            utilisateur.id_utilisateur
        )

        # THEN
        self.assertTrue(
            modification_ok, "La modification du mot de passe a échoué."
        )
        self.assertEqual(
            utilisateur_modifie.mot_de_passe,
            nouveau_mot_de_passe,
            "Le mot de passe n'a pas été correctement modifié.",
        )

    def test_supprimer_utilisateur(self):
        """Test de la suppression d'un utilisateur."""
        # GIVEN
        sel = creer_sel()
        mot_de_passe_hash = hacher_mot_de_passe("MotDePasseInitial", sel)
        utilisateur = Utilisateur(
            pseudo="UtilisateurASupprimer",
            adresse_email="asupprimer@example.com",
            mot_de_passe=mot_de_passe_hash,
            sel=sel,
        )
        self.utilisateur_dao.creer(utilisateur)
        # Enregistrer l'ID pour suppression après le test
        self.id_utilisateurs_crees.append(utilisateur.id_utilisateur)

        # WHEN
        suppression_ok = self.utilisateur_dao.supprimer_utilisateur(
            utilisateur.id_utilisateur
        )
        utilisateur_supprime = (
            self.utilisateur_dao.chercher_utilisateur_par_id(
                utilisateur.id_utilisateur
            )
        )

        # THEN
        self.assertTrue(
            suppression_ok, "La suppression de l'utilisateur a échoué."
        )
        self.assertIsNone(
            utilisateur_supprime,
            "L'utilisateur n'a pas été supprimé de la base de données.",
        )

    def test_lister_tous_les_utilisateurs(self):
        """Test de la liste de tous les utilisateurs."""
        # GIVEN
        sel1 = creer_sel()
        mot_de_passe_hash1 = hacher_mot_de_passe("MotDePasse1", sel1)
        utilisateur1 = Utilisateur(
            pseudo="Utilisateur1",
            adresse_email="user1@exemple.com",
            mot_de_passe=mot_de_passe_hash1,
            sel=sel1,
        )

        sel2 = creer_sel()
        mot_de_passe_hash2 = hacher_mot_de_passe("MotDePasse2", sel2)
        utilisateur2 = Utilisateur(
            pseudo="Utilisateur2",
            adresse_email="user2@exemple.com",
            mot_de_passe=mot_de_passe_hash2,
            sel=sel2,
        )

        # Création de deux utilisateurs
        self.utilisateur_dao.creer(utilisateur1)
        self.utilisateur_dao.creer(utilisateur2)
        # Enregistrer les IDs pour suppression après le test
        self.id_utilisateurs_crees.append(utilisateur1.id_utilisateur)
        self.id_utilisateurs_crees.append(utilisateur2.id_utilisateur)

        # WHEN
        utilisateurs_liste = (
            self.utilisateur_dao.lister_tous_les_utilisateurs()
        )

        # THEN
        self.assertGreaterEqual(
            len(utilisateurs_liste),
            2,
            "La liste des utilisateurs est incomplète.",
        )
        pseudos_utilisateurs = [user.pseudo for user in utilisateurs_liste]
        self.assertIn(
            "Utilisateur1",
            pseudos_utilisateurs,
            "Utilisateur1 n'est pas dans la liste des utilisateurs.",
        )
        self.assertIn(
            "Utilisateur2",
            pseudos_utilisateurs,
            "Utilisateur2 n'est pas dans la liste des utilisateurs.",
        )


if __name__ == "__main__":
    unittest.main()
