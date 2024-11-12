from src.data.db_connection import DBConnection
from src.Model.film import Film


class FilmDAO:
    """Classe contenant les méthodes pour créer,
    accéder et gérer les films dans la base de données"""

    # -------------------------------------------------------------------------
    # Méthodes
    # -------------------------------------------------------------------------

    """Création d'un film dans la base de données

        Parameters
        ----------
        film : Film
            Le film à créer

        Exception
        -------
        ValueError : erreur lors de la création du film dans la base.
    """
    def creer_film(self, film: Film):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO film(id_film,titre,genres,date_de_sortie,
                        langue_originale,synopsis)
                        VALUES (%(id_film)s, %(titre)s, %(genres)s,
                        %(date_de_sortie)s,%(langue_originale)s,
                        %(synopsis)s);
                        """,
                        {
                            "id_film": film.id_film,
                            "titre": film.titre,
                            "genres": film.genres,
                            "date_de_sortie": film.date_de_sortie,
                            "langue_originale": film.langue_originale,
                            "synopsis": film.synopsis,
                        },
                    )
        except Exception as e:
            raise ValueError(f"Erreur de la création du film : {str(e)}")

    """
    Lire un film dans la base de données.

    Parameters
    ----------
    id_film : int
        L'identifiant du film.

    Retour
    -------
    film : Film
        Le film recherché.

    Exception
    -------
    ValueError : erreur lors de la lecture du film dans la base.

    """
    def lire_film(self, id_film: int) -> Film:
        try:
            film = None
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM film
                        WHERE id_film=%(id_film)s;
                        """,
                        {
                            "id_film": id_film,
                        },
                    )
                    res = cursor.fetchone()
            if res:
                film = Film(
                    id_film=id_film,
                    titre=res["titre"],
                    genres=res["genres"],
                    date_de_sortie=res["date_de_sortie"],
                    langue_originale=res["langue_originale"],
                    synopsis=res["synopsis"],
                )
            return film
        except Exception as e:
            raise ValueError(f"Erreur de la lecture du film : {str(e)}")

    """
    Supprimer un film dans la base de données.

    Parameters
    ----------
    id_film : int
        L'identifiant du film.

    Exception
    -------
    ValueError : erreur lors de la suppression du film dans la base.

    """
    def supprimer_film(self, id_film: int):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE
                        FROM film
                        WHERE id_film=%(id_film)s;
                        """,
                        {
                            "id_film": id_film,
                        },
                    )
        except Exception as e:
            raise ValueError(f"Erreur de la suppression du film : {str(e)}")

    """
    Teste si un film est présent dans la base de données.

    Parameters
    ----------
    id_film : int
        L'identifiant du film.

    Retour
    ----------
    bool : True si le film est présent, False sinon.

    Exception
    -------
    ValueError : erreur lors du test dans la base.

    """
    def existe_film(self, id_film: int):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM film
                        WHERE id_film=%(id_film)s;
                        """,
                        {
                            "id_film": id_film,
                        },
                    )
                    if cursor.fetchone()["count"] == 1:
                        return True
                    return False
        except Exception as e:
            raise ValueError(f"Erreur du test : {str(e)}")

    """
    Renvoie des films présents dans la base. Le nombre est contrôlé par un
    paramètre "limite".

    Parameters
    ----------
    limite : int
        Le nombre de films maximum retournés.

    Retour
    ----------
    films : list[Film]
        La liste des films.

    Exception
    -------
    ValueError : erreur lors de la lecture des films dans la base.

    """
    def liste_films(self, limite: int = 100):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM film
                        LIMIT %(limite)s;
                        """,
                        {
                            "limite": limite,
                        }
                    )
                    res = cursor.fetchall()
                    films = []
                    for film in res:
                        films += [Film(id_film=film["id_film"],
                                       titre=film["titre"],
                                       genres=film["genres"],
                                       date_de_sortie=film["date_de_sortie"],
                                       langue_originale=film["langue_originale"],
                                       synopsis=film["synopsis"])]
                    return films
        except Exception as e:
            raise ValueError(f"Erreur lors de la lecture des films: {str(e)}")