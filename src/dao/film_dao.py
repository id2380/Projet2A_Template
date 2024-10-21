from datetime import datetime

from src.business_object.film import Film
from src.data.db_connection import DBConnection


class FilmDAO:
    """Classe contenant les méthodes pour créer,
    accéder et gérer les films dans la base de données"""

    def creer_film(self, film: Film) -> bool:
        """Création d'un film dans la base de données

        Parameters
        ----------
        film : Film
            Le film à créer

        Returns
        -------
        created : bool
            True si la création a réussi, False sinon
        """
<<<<<<< HEAD
        created = None
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO film(id_film,titre,genre,date_de_sortie,langue_originale,synopsis)
                    VALUES (%(id_film)s, %(titre)s, %(genre)s, %(date_de_sortie)s, %(langue_originale)s, %(synopsis)s)
                    RETURNING id_film;
                    """,
                    {
                        "id_film": film.id_film,
                        "titre": film.titre,
                        "genre": film.genre,
                        "date_de_sortie": film.date_de_sortie,
                        "langue_originale": film.langue_originale,
                        "synopsis": film.synopsis,
                    },
                )
                res = cursor.fetchone()
                if res:
                    film.id_film = res["id_film"]
                    created = True
=======
        created  = False
        try :
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO film(id_film,titre,genre,date_de_sortie,langue_originale,synopsis)
                        VALUES (%(id_film)s, %(titre)s, %(genre)s, %(date_de_sortie)s, %(langue_originale)s, %(synopsis)s)
                        RETURNING id_film;
                        """,
                        {
                            "id_film": film.id_film,
                            "titre": film.titre,
                            "genre": film.genre,
                            "date_de_sortie": film.date_de_sortie,
                            "langue_originale": film.langue_originale,
                            "synopsis": film.synopsis,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            return created
>>>>>>> 6572b1c79cc65b755f6994ee77b7ca9d55a03d63

        created = True
        return created
<<<<<<< HEAD

    def read_film(self, movieId: int) -> Film:
        """Lecture d'un film dans la base de données

        Parameters
        ----------
        movieId : int
            Identifiant du film à lire

        Returns
        -------
        Film
            Film à lire
        """
        film = None
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM film
                    WHERE id_film=%(movieId)s;
                    """,
                    {
                        "movieId": movieId,
                    },
                )
                res = cursor.fetchone()
        if res:
            film = Film(id_film=movieId,
                        titre=res["titre"],
                        genre=res["genre"],
                        date_de_sortie=res["date_de_sortie"],
                        langue_originale=res["langue_originale"],
                        synopsis=res["synopsis"],)
        return film

=======
>>>>>>> 6572b1c79cc65b755f6994ee77b7ca9d55a03d63
