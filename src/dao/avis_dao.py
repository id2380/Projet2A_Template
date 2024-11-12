from src.business_object.avis import Avis
from src.dao.film_dao import FilmDAO
from src.data.db_connection import DBConnection
from src.Model.utilisateur import Utilisateur
from src.service.film_service import FilmService


class AvisDAO:
    def creer_avis(self, avis: Avis) -> bool:
        try :
            film_service = FilmService()  
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    if not film_service.existe_film(avis.id_film):
                        print(
                            f"Le film avec l'ID '{avis.id_film}' n'a pas été trouvé dans la base. Création en cours via l'API TMDB..."
                        )
                        film_created = film_service.creer_film(avis.id_film)
                        if not film_created:
                            print(f"Impossible de créer le film avec l'ID '{avis.id_film}' via l'API TMDB.")
                            return False
                        print(f"Film avec l'ID '{avis.id_film}' créé avec succès.")

                    # Insertion de l'avis dans la base de données
                    cursor.execute(
                        """
                        INSERT INTO avis(id_film, utilisateur, note, commentaire)
                        VALUES (%s, %s, %s, %s) RETURNING id;
                    """,
                        (avis.id_film, avis.utilisateur, avis.note, avis.commentaire),
                    )
                    avis.id_avis = cursor.fetchone()[0]
                    connection.commit()
                    print(
                        f"Avis créé avec succès pour le film avec l'ID '{avis.id_film}' par l'utilisateur '{avis.utilisateur}'."
                    )
                    return True
        except Exception as e:
            print(f"Erreur lors de la création de l'avis : {e}")
        return False

    def modifier_avis(self, avis: Avis) -> bool:
        try:
            film_service = FilmService()  
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    if not film_service.existe_film(avis.id_film):
                        print(f"Le film avec l'ID '{avis.id_film}' n'existe pas dans la base de données.")
                        return False

                    # Vérification si l'utilisateur a déjà laissé un avis pour ce film
                    cursor.execute(
                        "SELECT id FROM avis WHERE id_film = %s AND utilisateur = %s;", (avis.id_film, avis.utilisateur)
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
                            "commentaire": avis.commentaire,
                        },
                    )

                    if cursor.rowcount == 0:
                        print(
                            f"Aucune modification effectuée pour l'avis du film {avis.id_film} par {avis.utilisateur}."
                        )
                        return False

                connection.commit()
                print(f"Avis modifié avec succès pour le film {avis.id_film} par l'utilisateur {avis.utilisateur}.")
                return True

        except Exception as e:
            print(f"Erreur lors de la modification de l'avis : {e}")
            return False

    def supprimer_avis(self, avis_id: int, utilisateur: str, id_film: int) -> bool:
        try:
            film_service = FilmService()  
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Vérifier si l'avis existe
                    cursor.execute(
                        "SELECT id FROM avis WHERE id = %s AND id_film = %s AND utilisateur = %s;",
                        (avis_id, id_film, utilisateur),
                    )
                    avis = cursor.fetchone()

                    if cursor.fetchone() is None:
                        print("Aucun avis trouvé.")
                        return False

                    # Suppression de l'avis
                    cursor.execute(
                        "DELETE FROM avis WHERE id = %s AND id_film = %s AND utilisateur = %s;",
                        (avis_id, id_film, utilisateur),
                    )

                    # Vérifier si la suppression a affecté une ligne
                    if cursor.rowcount == 0:
                        print(f"Aucun avis supprimé pour l'utilisateur {utilisateur} sur le film {id_film}.")
                        return False  # Aucune ligne supprimée, renvoyer False

                connection.commit()
                print(f"Avis supprimé avec succès pour {utilisateur} sur le film {id_film}.")
                return True  # Avis supprimé avec succès

        except Exception as e:
            print(f"Erreur lors de la suppression de l'avis : {e}")
        return False  # En cas d'erreur, renvoyer False

    def lire_avis(self, id_film=None, utilisateur=None, id_utilisateur=None) -> list:
        try:
            film_service = FilmService()  
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    query = "SELECT * FROM avis"
                    conditions = []
                    params = []

                    if id_film is not None:
                        conditions.append("id_film = %s")
                        params.append(id_film)
                    if utilisateur is not None:
                        conditions.append("utilisateur = %s")
                        params.append(utilisateur)
                    if id_utilisateur is not None:
                        conditions.append("id_utilisateur = %s")
                        params.append(id_utilisateur)
                
                    if conditions:
                        query += " WHERE " + " AND ".join(conditions)
                
                    cursor.execute(query, tuple(params))
                    result = cursor.fetchall()

                    # Si aucun résultat n'est trouvé, renvoyer une liste vide
                    if not result:
                        return []

                    # Si des avis sont trouvés, les transformer en objets Avis
                    return [Avis(*row) for row in result]  # Assurez-vous que le constructeur Avis peut prendre un tuple directement

        except Exception as e:
            print(f"Erreur lors de la lecture des avis : {e}")
            return []  # Retourner une liste vide en cas d'erreur
