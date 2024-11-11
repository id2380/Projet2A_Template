from src.dao.utilisateur_dao import UtilisateurDAO
from src.data.db_connection import DBConnection
from src.Model.utilisateur import Utilisateur
from src.utils.singleton import Singleton


class EclaireurDAO(metaclass=Singleton):
    """
    Une classe qui permet de manipuler les éclaireurs dans la base de données.
    """

    # -------------------------------------------------------------------------
    # Méthodes
    # -------------------------------------------------------------------------

    """
        Permet à un utiliseur de s'abonner à un autre utilisateur. En cas de
        problème, une erreur est rendue.

        Paramètres
        ----------
        id_utilisateur : int
            L'identifiant unique qui correspond à l'utilisateur qui souhaite
            s'abonner à l'autre utilisateur.
        id_eclaireur : int
            L'identifiant unique qui correspond à l'utilisateur auquel l'autre
            utilisateur souhaite s'abonner.

        Retour
        ----------
        None : l'utilisateur a correctement été ajouté
        ValueError : erreur si problème pendant l'ajout

        """
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
                        {"id_utilisateur": id_utilisateur, "id_eclaireur":
                         id_eclaireur},
                    )
        except Exception as e:
            raise ValueError(f"Erreur lors de l'ajout de l'éclaireur : {e}")

    """
        Permet de savoir si un utilisateur est abonné à un autre.

        Paramètres
        ----------
        id_utilisateur : int
            L'identifiant unique qui correspond à l'utilisateur qui est supposé
            abonné à l'autre utilisateur.
        id_eclaireur : int
            L'identifiant unique qui correspond à l'utilisateur auquel l'autre
            utilisateur est supposé abonné.

        Retour
        ----------
        boolean : indique si l'utilisateur est abonné à l'autre
        ValueError : erreur si problème pendant la vérification
        """
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
                        {"id_utilisateur": id_utilisateur, "id_eclaireur":
                         id_eclaireur},
                    )
                    if cursor.fetchone()["count"] == 1:
                        return True
                    return False
        except Exception as e:
            raise ValueError(f"Erreur lors de la vérification de l'abonnement : {e}")

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
                        {"id_utilisateur": id_utilisateur},
                    )
                    res = cursor.fetchall()
                    return [d["id_eclaireur"] for d in res]
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
                        {"id_utilisateur": id_utilisateur, "id_eclaireur": id_eclaireur},
                    )
        except Exception as e:
            raise ValueError(f"Erreur lors de la suppression de l'éclaireur : {e}")

