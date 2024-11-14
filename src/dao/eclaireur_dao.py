from src.data.db_connection import DBConnection
from src.utils.singleton import Singleton


class EclaireurDAO(metaclass=Singleton):
    """
    Une classe qui permet de manipuler les éclaireurs dans la base de données.
    """

    # -------------------------------------------------------------------------
    # Méthodes
    # -------------------------------------------------------------------------

    def ajouter_eclaireur(self, id_utilisateur: int, id_eclaireur: int):
        """
        Permet à un utilisateur de s'abonner à un éclaireur.

        Paramètres
        ----------
        id_utilisateur : int
            L'identifiant unique de l'utilisateur qui souhaite s'abonner.
        id_eclaireur : int
            L'identifiant unique de l'utilisateur auquel on souhaite s'abonner.

        Exception
        ----------
        ValueError : si une erreur survient lors de l'ajout de l'abonnement.
        """
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

    def est_eclaireur(self, id_utilisateur: int, id_eclaireur: int):
        """
        Vérifie si un utilisateur est abonné à un éclaireur.

        Paramètres
        ----------
        id_utilisateur : int
            L'identifiant unique de l'utilisateur pour lequel l'abonnement est
            vérifié.
        id_eclaireur : int
            L'identifiant unique de l'utilisateur qui est supposé être suivi
            par l'utilisateur.

        Retour
        ----------
        bool : True si l'utilisateur est abonné à l'éclaireur, False sinon.

        Exception
        ----------
        ValueError : si une erreur survient lors du test de l'abonnement.
        """
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
        """
        Renvoie la liste des éclaireurs auxquels un utilisateur est abonné.

        Paramètres
        ----------
        id_utilisateur : int
            L'identifiant unique de l'utilisateur pour lequel on souhaite obtenir
            la liste de ses éclaireurs.

        Retour
        ----------
        list : liste des identifiants des éclaireurs associés à l'utilisateur.

        Exception
        ----------
        ValueError : si une erreur survient lors de la récupération des
        identifiants.
        """
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
        """
        Supprime l'abonnement d'un utilisateur à un éclaireur.

        Paramètres
        ----------
        id_utilisateur : int
            L'identifiant unique de l'utilisateur pour lequel on souhaite
            supprimer l'abonnement.
        id_eclaireur : int
            L'identifiant unique de l'éclaireur dont on souhaite supprimer
            l'abonnement.

        Exception
        ----------
        ValueError : si une erreur survient lors de la suppression.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM abonne
                        WHERE id_utilisateur = %(id_utilisateur)s
                        AND id_eclaireur = %(id_eclaireur)s
                        """,
                        {"id_utilisateur": id_utilisateur, "id_eclaireur":
                         id_eclaireur},
                    )
        except Exception as e:
            raise ValueError(f"Erreur lors de la suppression de l'éclaireur : {e}")