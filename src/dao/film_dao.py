from src.Model.film import Film
from src.data.db_connection import DBConnection
from datetime import datetime


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
        bool
            True si la création a réussi, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO film(id_film,titre,genre,date_de_sortie,
                        langue_originale,synopsis)
                        VALUES (%(id_film)s, %(titre)s, %(genre)s,
                        %(date_de_sortie)s, %(langue_originale)s, %(synopsis)s)
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
        except Exception:
            return False
        return True

    def lire_film(self, id_film: int) -> Film:
        """Lecture d'un film dans la base de données

        Parameters
        ----------
        id_film : int
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
                    WHERE id_film=%(id_film)s;
                    """,
                    {
                        "id_film": id_film,
                    },
                )
                res = cursor.fetchone()
        if res:
            film = Film(id_film=id_film,
                        titre=res["titre"],
                        genre=res["genre"],
                        date_de_sortie=res["date_de_sortie"],
                        langue_originale=res["langue_originale"],
                        synopsis=res["synopsis"])
        return film

    def parse_str(self,date:str):
        if date != '':
            return datetime.strptime(date, "%Y-%m-%d")
        return None

    def supprimer_film(self, id_film: int) -> bool:
        """Suppression d'un film dans la base de données

        Parameters
        ----------
        id_film : int
            Identifiant du film à supprimer

        Returns
        -------
        bool
            True si le film a bien été supprimé, False sinon
        """
        if self.lire_film(id_film) is None:  # film n'existe pas
            return False

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
        return True
if __name__ == "__main__":
    # Pour charger les variables d'environnement contenues dans le fichier .env
   

    film_client = FilmDAO()
    film = Film(id_film=1,
                titre="Test",
                genre="",
                date_de_sortie=None,
                langue_originale="",
                synopsis="")
    
    # boolean = film_client.creer_film(film)
    boolean = film_client.supprimer_film(1)
    print(boolean)