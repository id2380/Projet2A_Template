from src.business_object.avis import Avis
from src.business_object.film import Film
from src.business_object.utilisateur import Utilisateur
from src.dao.utilisateur_dao import UtilisateurDAO
from src.data.db_connection import DBConnection
from src.Service.film_service import FilmService
from src.dao.film_dao import FilmDAO

class AvisDAO:

    
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
        """
        Modification d'un avis existant pour un utilisateur spécifique et un film spécifique.
        La fonction vérifie d'abord si le film et l'avis existent dans la base de données.

        Parameters
        ----------
        avis : Avis
            L'avis à modifier, qui inclut l'ID du film, le pseudo de l'utilisateur, la note et le commentaire.

        Returns
        -------
        updated : bool
            True si la modification a réussi, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Vérification si le film existe dans la base de données
                    cursor.execute("SELECT id_film FROM film WHERE id_film = %s;", (avis.id_film,))
                    film_exist = cursor.fetchone()
                
                    if not film_exist:
                        print(f"Le film avec l'ID '{avis.id_film}' n'existe pas dans la base de données.")
                        return False

                    # Vérification si l'utilisateur a déjà laissé un avis pour ce film
                    cursor.execute(
                        "SELECT id FROM avis WHERE id_film = %s AND utilisateur = %s;", 
                        (avis.id_film, avis.utilisateur)
                    )
                    avis_exist = cursor.fetchone()

                    if not avis_exist:
                        print(f"Aucun avis trouvé pour le film {avis.id_film} par l'utilisateur {avis.utilisateur}.")
                        return False

                    # Si le film et l'avis existent, procéder à la modification
                    cursor.execute(
                        """
                        UPDATE avis
                        SET note = %(note)s, commentaire = %(commentaire)s
                        WHERE id_film = %(id_film)s AND utilisateur = %(utilisateur)s;
                        """,
                        {
                            "id_film": avis.id_film,
                            "utilisateur": avis.utilisateur,
                            "note": avis.note,
                            "commentaire": avis.commentaire
                        }
                    )

            connection.commit()

            if cursor.rowcount == 0:
                print(f"Aucune modification effectuée pour l'avis du film {avis.id_film} par {avis.utilisateur}.")
                return False

            print(f"Avis modifié avec succès pour le film {avis.id_film} par l'utilisateur {avis.utilisateur}.")
            return True

        except Exception as e:
            print(f"Erreur lors de la modification de l'avis : {e}")
            return False


    def supprimer_avis(self, avis_id: int, utilisateur: str, id_film: int) -> bool:
        """
        Suppression d'un avis dans la base de données pour un utilisateur et un film spécifiques.
        Supprime également le film si plus aucun avis n'existe pour ce film.

        Parameters
        ----------
        avis_id : int
            L'identifiant de l'avis à supprimer.
        utilisateur : str
            Le pseudo de l'utilisateur qui a posté l'avis.
        id_film : int
            L'identifiant du film auquel l'avis est associé.

        Returns
        -------
        deleted : bool
            True si la suppression a réussi, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Vérification si l'avis existe pour cet utilisateur et ce film
                    cursor.execute(
                        "SELECT id FROM avis WHERE id = %s AND utilisateur = %s AND id_film = %s;",
                        (avis_id, utilisateur, id_film)
                    )
                    avis_exist = cursor.fetchone()

                    if not avis_exist:
                        print(f"Avis {avis_id} inexistant pour l'utilisateur {utilisateur} et le film {id_film}.")
                        return False

                    # Suppression de l'avis
                    cursor.execute(
                        "DELETE FROM avis WHERE id = %(id)s AND utilisateur = %(utilisateur)s AND id_film = %(id_film)s;",
                        {"id": avis_id, "utilisateur": utilisateur, "id_film": id_film}
                    )

                    if cursor.rowcount == 0:
                        print(f"Échec de la suppression de l'avis {avis_id}.")
                        return False

                    # Vérification s'il reste d'autres avis pour ce film
                    cursor.execute("SELECT COUNT(*) FROM avis WHERE id_film = %s;", (id_film,))
                    avis_restants = cursor.fetchone()[0]

                    if avis_restants == 0:
                        # Suppression du film s'il n'y a plus d'avis pour ce film
                        film_dao = FilmDAO()
                        film_deleted = film_dao.supprimer_film(id_film)
                        if film_deleted:
                            print(f"Film {id_film} supprimé car plus aucun avis n'existe.")
                        else:
                            print(f"Le film {id_film} n'a pas pu être supprimé.")

                connection.commit()
                print(f"Avis {avis_id} supprimé avec succès pour l'utilisateur {utilisateur} et le film {id_film}.")
                return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'avis : {e}")
            return False


    
    def lire_avis(self, id_film: int, utilisateur: str = None):
        """
        Lecture des avis dans la base de données basée sur l'ID du film, et éventuellement le pseudo de l'utilisateur.

        Parameters
        ----------
        id_film : int
            L'ID du film pour lequel consulter les avis.
        utilisateur : str, optional
            Le nom de l'utilisateur pour lequel consulter son propre avis (facultatif).

        Returns
        -------
        avis_list : list of Avis
            Une liste des avis récupérés. Si aucun avis n'est trouvé, retourne un message indiquant qu'il n'y a pas d'avis.
        """
        avis_list = []
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    if utilisateur:
                        # L'utilisateur souhaite lire son propre avis pour un film spécifique
                        query = "SELECT * FROM avis WHERE id_film = %s AND utilisateur = %s;"
                        cursor.execute(query, (id_film, utilisateur))
                    else:
                        # L'utilisateur souhaite lire tous les avis pour un film spécifique
                        query = "SELECT * FROM avis WHERE id_film = %s;"
                        cursor.execute(query, (id_film,))

                    rows = cursor.fetchall()
                    if not rows:
                        # Aucun avis trouvé
                        print(f"Aucun avis trouvé pour le film avec l'ID {id_film}.")
                        return "Aucun avis trouvé."

                    for row in rows:
                        avis = Avis(
                            id_avis=row['id'],
                            id_film=row['id_film'],
                            utilisateur=row['utilisateur'],
                            note=row['note'],
                            commentaire=row['commentaire']
                        )
                        avis_list.append(avis)

                return avis_list
        except Exception as e:
            print(f"Erreur lors de la lecture des avis : {e}")
            return "Erreur lors de la lecture des avis."
