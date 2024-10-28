from src.dao.utilisateur_dao import UtilisateurDAO
from src.data.db_connection import DBConnection
from src.Model.utilisateur import Utilisateur
from src.utils.singleton import Singleton


class EclaireurDAO(metaclass=Singleton):
    def ajouter_eclaireur(self, id_utilisateur: int, id_eclaireur: int):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO abonne(id_utilisateur, id_eclaireur)
                        VALUES (%(id_utilisateur)s, %(id_eclaireur)s)
                        RETURNING id_utilisateur
                        """,
                        {'id_utilisateur': id_utilisateur,
                            'id_eclaireur': id_eclaireur}
                    )
        except Exception as e:
            raise ValueError(f"Erreur lors de l'ajout de l'éclaireur : {e}")

    def est_eclaireur(self, id_utilisateur: int, id_eclaireur: int):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM abonne
                        WHERE id_utilisateur = %(id_utilisateur)s AND
                        id_eclaireur =%(id_eclaireur)s
                        """,
                        {'id_utilisateur': id_utilisateur,
                            'id_eclaireur': id_eclaireur}
                    )
                    if cursor.fetchone()["count"] == 1:
                        return True
                    return False
        except Exception as e:
            raise ValueError(f"Erreur lors de l'abonnement avec l'éclaireur : {e}")

    def liste_eclaireurs(self, id_utilisateur: int):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM abonne
                        WHERE id_utilisateur = %(id_utilisateur)s
                        """,
                        {'id_utilisateur': id_utilisateur}
                    )
                    res = cursor.fetchall()
                    return [d['id_eclaireur'] for d in res]
        except Exception as e:
            raise ValueError(f"Erreur lors de la recherche des éclaireurs : {e}")

    def supprimer_eclaireur(self, id_utilisateur: int, id_eclaireur: int):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM abonne
                        WHERE id_utilisateur = %(id_utilisateur)s
                        AND id_eclaireur = %(id_eclaireur)s
                        """,
                        {'id_utilisateur': id_utilisateur,
                         'id_eclaireur': id_eclaireur}
                    )
        except Exception as e:
            raise ValueError(f"Erreur lors de la suppression de l'éclaireur : {e}")


if __name__ == "__main__":
    # Initialisation d'un utilisateur et d'un éclaireur
    utilisateur = Utilisateur(pseudo="Jules",
                              adresse_email="jules@",
                              mot_de_passe="mdp",
                              sel="sel")
    eclaireur = Utilisateur(pseudo="Eclaireur",
                            adresse_email="éclaireur@",
                            mot_de_passe="mdp",
                            sel="sel")
    eclaireur2 = Utilisateur(pseudo="Eclaireur2",
                             adresse_email="éclaireur2@",
                             mot_de_passe="mdp",
                             sel="sel")
    eclaireur3 = Utilisateur(pseudo="Eclaireur3",
                             adresse_email="éclaireur3@",
                             mot_de_passe="mdp",
                             sel="sel")
    # Création en base des utilisateurs
    utilisateur_dao = UtilisateurDAO()
    # utilisateur_dao.creer(utilisateur)
    # utilisateur_dao.creer(eclaireur)
    # utilisateur_dao.creer(eclaireur2)
    # utilisateur_dao.creer(eclaireur3)
    # Création de la DAo éclaireur
    eclaireur_dao = EclaireurDAO()
    """
    eclaireur_dao.ajouter_eclaireur(utilisateur_dao.chercher_utilisateur_par_pseudo(utilisateur.pseudo).id_utilisateur,
                                    utilisateur_dao.chercher_utilisateur_par_pseudo(eclaireur.pseudo).id_utilisateur)
    eclaireur_dao.ajouter_eclaireur(12,
                                    utilisateur_dao.chercher_utilisateur_par_pseudo(eclaireur.pseudo).id_utilisateur)
    
    eclaireur_dao.ajouter_eclaireur(utilisateur_dao.chercher_utilisateur_par_pseudo(utilisateur.pseudo).id_utilisateur,
                                    utilisateur_dao.chercher_utilisateur_par_pseudo(eclaireur2.pseudo).id_utilisateur)
    
    print(eclaireur_dao.est_eclaireur(utilisateur_dao.chercher_utilisateur_par_pseudo(utilisateur.pseudo).id_utilisateur,
                                      utilisateur_dao.chercher_utilisateur_par_pseudo(eclaireur.pseudo).id_utilisateur))
    print(eclaireur_dao.est_eclaireur(utilisateur_dao.chercher_utilisateur_par_pseudo(utilisateur.pseudo).id_utilisateur,
                                      utilisateur_dao.chercher_utilisateur_par_pseudo(eclaireur3.pseudo).id_utilisateur))
    print(eclaireur_dao.liste_eclaireurs(utilisateur_dao.chercher_utilisateur_par_pseudo(utilisateur.pseudo).id_utilisateur))
    eclaireur_dao.ajouter_eclaireur(utilisateur_dao.chercher_utilisateur_par_pseudo(utilisateur.pseudo).id_utilisateur,
                                    utilisateur_dao.chercher_utilisateur_par_pseudo(eclaireur3.pseudo).id_utilisateur)
    eclaireur_dao.supprimer_eclaireur(utilisateur_dao.chercher_utilisateur_par_pseudo(utilisateur.pseudo).id_utilisateur,
                                      utilisateur_dao.chercher_utilisateur_par_pseudo(eclaireur3.pseudo).id_utilisateur)
    
    """

    