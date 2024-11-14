from src.data.db_connection import DBConnection
from src.Model.avis import Avis


class AvisDAO:
    """
    Classe contenant les méthodes pour créer,accéder et gérer les films dans
    la base de données.
    """

    # -------------------------------------------------------------------------
    # Méthodes
    # -------------------------------------------------------------------------

    def creer_avis(self, avis: Avis):
        """
        Création d'un avis dans la base de données.

        Parameters
        ----------
        avis : Avis
            L'avis à créer.

        Exception
        -------
        ValueError : erreur lors de la création de l'avis dans la base.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO avis(id_film, id_utilisateur, note,
                        commentaire) VALUES (%s, %s, %s, %s);
                        """,
                        (avis.id_film, avis.id_utilisateur, avis.note,
                         avis.commentaire),
                    )
        except Exception as e:
            raise ValueError(f"Erreur lors de la création de l'avis : {e}")

    def modifier_avis(self, avis: Avis):
        """
        Modification d'un avis dans la base de données.

        Parameters
        ----------
        avis : Avis
            L'avis à modifier.

        Exception
        -------
        ValueError : erreur lors de la modification de l'avis dans la base.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE avis
                        SET note = %(note)s, commentaire = %(commentaire)s
                        WHERE id_film = %(id_film)s
                        AND id_utilisateur = %(id_utilisateur)s;
                        """,
                        {
                            "id_film": avis.id_film,
                            "id_utilisateur": avis.id_utilisateur,
                            "note": avis.note,
                            "commentaire": avis.commentaire,
                        },
                    )
        except Exception as e:
            raise ValueError(f"Erreur lors de la modification de l'avis : {e}")

    def supprimer_avis(self,  id_film: int, id_utilisateur: int):
        """
        Suppression d'un avis dans la base de données.

        Parameters
        ----------
        id_film : int
            L'id du film associé à l'avis à supprimer.

        id_utilisateur : int
            L'id de l'utilisateur associé à l'avis à supprimer.

        Exception
        -------
        ValueError : erreur lors de la suppression de l'avis dans la base.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """DELETE FROM avis WHERE  id_film = %s
                         AND id_utilisateur = %s;""",
                        (id_film, id_utilisateur),
                    )
        except Exception as e:
            raise ValueError(f"Erreur lors de la suppression de l'avis : {e}")

    def existe_avis(self, id_film: int, id_utilisateur: int):
        """
        Vérifie si un avis existe dans la base de données.

        Parameters
        ----------
        id_film : int
            L'id du film associé à l'avis.

        id_utilisateur : int
            L'id de l'utilisateur associé à l'avis.

        Return
        ----------
        bool : True, si l'avis existe, sinon False.

        Exception
        -------
        ValueError : erreur lors de la vérification dans la base.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM avis
                        WHERE id_film = %s AND id_utilisateur = %s;
                        """,
                        (id_film, id_utilisateur),
                    )
                    if cursor.fetchone()["count"] == 1:
                        return True
                    return False
        except Exception as e:
            raise ValueError(f"Erreur lors du test d'existence de l'avis : {e}")

    def lire_avis(self, id_film=None, id_utilisateur=None):
        """
        Recherche d'avis dans la base de données. Cette recherche peut être
        fait en ciblant les avis liés à un film, à un utilisateur ou les deux.

        Parameters
        ----------
        id_film : int
            L'id du film associé aux avis à rechercher.

        id_utilisateur : int
            L'id de l'utilisateur aux avis à rechercher.

        Return
        ----------
        avis : list[Avis]
            La liste des avis recherchés.

        Exception
        -------
        ValueError : erreur lors de la recherche d'avis dans la base.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    query = """SELECT a.id_film, a.id_utilisateur, a.note,
                               a.commentaire FROM avis a """
                    conditions = []
                    params = []
                    if id_film is not None:
                        conditions.append("a.id_film = %s")
                        params.append(id_film)

                    if id_utilisateur is not None:
                        conditions.append("a.id_utilisateur = %s")
                        params.append(id_utilisateur)
                    if conditions:
                        query += " WHERE " + " AND ".join(conditions)
                    cursor.execute(query, tuple(params))
                    res = cursor.fetchall()
                    avis = []
                    for a in res:
                        avis += [Avis(id_film=a["id_film"],
                                      id_utilisateur=a["id_utilisateur"],
                                      note=a["note"],
                                      commentaire=a["commentaire"])]
                    return avis
        except Exception as e:
            raise ValueError(f"Erreur lors de la recherche des avis : {e}")

    def lire_avis_eclaireurs(self, id_film: int, liste_id: list):
        """
        Recherche d'avis dans la base de données. Les avis recupérés sont ceux
        associés au film passé en paramètre et à un des identifiants
        d'utilisateur présent dans la liste.

        Parameters
        ----------
        id_film : int
            L'id du film associé aux avis à rechercher.

        liste_id : list[int]
            La liste d'identifiant potentiellement associés aux avis.

        Return
        ----------
        avis : list[Avis]
            La liste des avis recherchés.

        Exception
        -------
        ValueError : erreur lors de la recherche d'avis dans la base.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM avis
                        WHERE id_film = %s AND id_utilisateur = ANY(%s);
                        """,
                        (id_film,  liste_id),
                    )
                    res = cursor.fetchall()
                    avis = []
                    for a in res:
                        avis += [Avis(id_film=a["id_film"],
                                      id_utilisateur=a["id_utilisateur"],
                                      note=a["note"],
                                      commentaire=a["commentaire"])]
                    return avis
        except Exception as e:
            raise ValueError(f"Erreur lors de la recherche des avis : {e}")

    def lire_avis_communs(self, id_utilisateur1: int, id_utilisateur2: int):
        """
        Recherche les avis associés à un même film pour deux utilisateurs.

        Parameters
        ----------
        id_utilisateur1 : int
            L'id du premier utilisateur.

        id_utilisateur2 : int
            L'id du second utilisateur.

        Return
        ----------
        avis : list[dict{"Avis1": Avis, "Avis2": Avis}]
            La liste des dictionnaires des avis associés au même film.

        Exception
        -------
        ValueError : erreur lors de la recherche d'avis dans la base.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT a1.id_film,
                        a1.id_utilisateur AS id_utilisateur1,
                        a2.id_utilisateur AS id_utilisateur2,
                        a1.note AS note1,
                        a2.note AS note2,
                        a1.commentaire AS commentaire1,
                        a2.commentaire AS commentaire2
                        FROM avis a1
                        JOIN avis a2 ON a1.id_film = a2.id_film
                        WHERE a1.id_utilisateur = %s AND a2.id_utilisateur = %s
                        """,
                        (id_utilisateur1,  id_utilisateur2),
                    )
                    res = cursor.fetchall()
                    avis = []
                    for a in res:
                        avis += [{"Avis 1": Avis(id_film=a["id_film"],
                                                 id_utilisateur=a["id_utilisateur1"],
                                                 note=a["note1"],
                                                 commentaire=a["commentaire1"]),
                                  "Avis 2": Avis(id_film=a["id_film"],
                                                 id_utilisateur=a["id_utilisateur2"],
                                                 note=a["note2"],
                                                 commentaire=a["commentaire2"])}]
                    return avis
        except Exception as e:
            raise ValueError(f"Erreur lors de la recherche des avis : {e}")