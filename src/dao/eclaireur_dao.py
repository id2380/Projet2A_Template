from src.data.db_connection import DBConnection
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