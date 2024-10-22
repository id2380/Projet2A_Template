from src.business_object.avis import Avis
from src.business_object.film import Film
from src.business_object.Utilisateur import Utilisateur
from src.dao.utilisateur_dao import UtilisateurDAO
from src.data.db_connection import DBConnection
from src.Service.film_service import FilmService


class AvisDAO:

    """Classe contenant les méthodes pour créer, consulter, modifier et supprimer des avis dans la base de données."""
    def __init__(self, film_service: FilmService, utilisateur_dao: UtilisateurDAO):
        self.film_service = film_service
        self.utilisateur_dao = utilisateur_dao
    def creer_avis(self, avis: Avis) -> bool:
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                 # Vérification si le film existe dans la base de données via l'id_film fourni
                    cursor.execute("SELECT id_film FROM film WHERE id_film = %s;", (avis.id_film,))
                    if not cursor.fetchone():
                        print(f"Le film avec l'ID '{avis.id_film}' n'a pas été trouvé dans la base. Création en cours via l'API TMDB...")
                        if not self.film_service.creer_film(avis.id_film):
                            print(f"Impossible de créer le film avec l'ID '{avis.id_film}' via l'API TMDB.")
                            return False
                        print(f"Film avec l'ID '{avis.id_film}' créé avec succès.")

                    # Insertion de l'avis dans la base de données sans vérifier l'utilisateur
                    cursor.execute("""
                        INSERT INTO avis(id_film, utilisateur, note, commentaire)
                        VALUES (%s, %s, %s, %s) RETURNING id;
                    """, (avis.id_film, avis.utilisateur, avis.note, avis.commentaire))

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
