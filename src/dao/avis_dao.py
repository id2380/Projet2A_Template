from src.business_object.avis import Avis
from src.business_object.film import Film
from src.business_object.utilisateur import Utilisateur
from src.data.db_connection import DBConnection
from src.Service.filmservice import FilmService


class AvisDAO:

    """Classe contenant les méthodes pour créer, consulter, modifier et supprimer des avis dans la base de données."""
    def __init__(self, film_service: FilmService, utilisateur_dao: UtilisateurDAO):
        self.film_service = film_service
        self.utilisateur_dao = utilisateur_dao
    def creer_avis(self, avis: Avis) -> bool:
        """
        Création d'un avis dans la base de données. L'utilisateur fournit l'ID du film (id_film) au lieu du titre du film.

        Parameters
        ----------
        avis : Avis
            L'avis à créer, qui inclut l'id_film, l'utilisateur, la note, et le commentaire.

        Returns
        -------
        bool
            True si l'avis a été créé avec succès, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:

                    # Vérification si le film existe dans la base de données via l'id_film fourni
                    cursor.execute("SELECT id_film FROM film WHERE id_film = %s;", (avis.id_film,))
                    film = cursor.fetchone()

                    # Si le film n'existe pas, le créer avec l'API TMDB via FilmService
                    if film is None:
                        print(f"Le film avec l'ID '{avis.id_film}' n'a pas été trouvé dans la base. Création en cours via l'API TMDB...")
                        film = self.film_service.creer_film(avis.id_film)
                        if film is None:
                            raise ValueError(f"Impossible de créer le film avec l'ID '{avis.id_film}' via l'API TMDB.")
                        print(f"Film avec l'ID '{film.id_film}' créé avec succès.")

                    # Vérification si l'utilisateur existe
                    utilisateur = self.utilisateur_dao.read(avis.utilisateur)
                    if utilisateur is None:
                        raise ValueError(f"L'utilisateur '{avis.utilisateur}' n'existe pas.")

                    # Insertion de l'avis dans la base de données
                    cursor.execute(
                        """
                        INSERT INTO avis(id_film, utilisateur, note, commentaire, id_utilisateur)
                        VALUES (%(id_film)s, %(utilisateur)s, %(note)s, %(commentaire)s, %(id_utilisateur)s)
                        RETURNING id;
                        """,
                        {
                            "id_film": avis.id_film,
                            "utilisateur": utilisateur.pseudo,
                            "note": avis.note,
                            "commentaire": avis.commentaire,
                            "id_utilisateur": utilisateur.id_utilisateur
                        }
                    )

                    # Récupérer l'ID de l'avis nouvellement créé
                    avis.id_avis = cursor.fetchone()[0]
                    connection.commit()
                    print(f"Avis créé avec succès pour le film avec l'ID '{avis.id_film}' par l'utilisateur '{avis.utilisateur}'.")
                    return True

        except Exception as e:
            print(f"Erreur lors de la création de l'avis : {e}")
            return False



    

    def modifier_avis(self, avis: Avis) -> bool:
        """Modification d'un avis existant dans la base de données.

        Parameters
        ----------
        avis : Avis
            L'avis à modifier

        Returns
        -------
        updated : bool
            True si la modification a réussi, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE avis
                        SET note = %(note)s, commentaire = %(commentaire)s
                        WHERE id = %(id)s;
                        """,
                        {
                            "id": avis.id,
                            "note": avis.note,
                            "commentaire": avis.commentaire,
                        }
                    )
            connection.commit()
            print(f"Avis {avis.id} modifié avec succès.")
            return True
        except Exception as e:
            print(f"Erreur lors de la modification de l'avis : {e}")
            return False

    def supprimer_avis(self, avis_id: int) -> bool:
        """Suppression d'un avis dans la base de données.

        Parameters
        ----------
        avis_id : int
            L'identifiant de l'avis à supprimer

        Returns
        -------
        deleted : bool
            True si la suppression a réussi, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM avis WHERE id = %(id)s;",
                        {"id": avis_id}
                    )
                    if cursor.rowcount == 0:
                        # Si aucune ligne n'a été supprimée, l'avis n'existait pas
                        print(f"Avis {avis_id} inexistant.")
                        return False
                connection.commit()
                print(f"Avis {avis_id} supprimé avec succès.")
                return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'avis : {e}")
            return False
    
    def lire_avis(self, avis_id=None, film=None, utilisateur=None):
        """Lecture des avis dans la base de données basée sur un ID d'avis, un titre de film, ou un nom d'utilisateur.

        Parameters
        ----------
        avis_id : int, optional
            L'ID de l'avis spécifique à consulter.
        film : str, optional
            Le titre du film pour lequel consulter les avis.
        utilisateur : str, optional
            Le nom de l'utilisateur pour lequel consulter les avis.

        Returns
        -------
        avis_list : list of Avis
            Une liste des avis récupérés.
        """
        avis_list = []
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    if avis_id:
                        query = "SELECT * FROM avis WHERE id = %s;"
                        cursor.execute(query, (avis_id,))
                    elif film:
                        query = "SELECT * FROM avis WHERE film = %s;"
                        cursor.execute(query, (film,))
                    elif utilisateur:
                        query = "SELECT * FROM avis WHERE utilisateur = %s;"
                        cursor.execute(query, (utilisateur,))
                    else:
                        return avis_list  # Retourne une liste vide si aucun critère n'est fourni

                    rows = cursor.fetchall()
                    for row in rows:
                        avis = Avis(
                            id=row['id'], 
                            film=row['film'], 
                            utilisateur=row['utilisateur'],
                            note=row['note'], 
                            commentaire=row['commentaire']
                        )
                        avis_list.append(avis)
            return avis_list
        except Exception as e:
            print(f"Erreur lors de la lecture des avis : {e}")
            return avis_list
