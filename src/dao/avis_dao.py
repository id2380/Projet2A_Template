from src.business_object.avis import Avis
from src.dao.film_dao import FilmDAO
from src.data.db_connection import DBConnection
from src.Model.utilisateur import Utilisateur
from src.service.film_service import FilmService


class AvisDAO:
    def creer_avis(self, avis: Avis) -> bool:
        try :
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Insertion de l'avis dans la base de données
                    cursor.execute(
                        """
                        INSERT INTO avis(id_film, utilisateur, note, commentaire)
                        VALUES (%s, %s, %s, %s) RETURNING id;
                    """,
                        (avis.id_film, avis.utilisateur, avis.note, avis.commentaire),
                    )
                    result = cursor.fetchone()
                    if result:
                        avis.id_avis = result['id']
                        connection.commit()
                        return f"Avis créé avec succès pour le film avec l'ID '{avis.id_film}' par l'utilisateur '{avis.utilisateur}'."
                        
                    else:
                        return "Aucun ID retourné pour l'avis créé."
        except Exception as e:
            print(f"Erreur lors de la création de l'avis : {e}")
        return False
    
    def modifier_avis(self, avis: Avis) -> bool:
        try:

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                    """
                    SELECT id FROM avis
                    WHERE id_film = %s AND utilisateur = %s;
                    """,
                    (avis.id_film, avis.utilisateur)
                )
                
                    if cursor.fetchone() is None:
                        return f"Aucun avis trouvé pour le film {avis.id_film} par l'utilisateur {avis.utilisateur}."
                        return False

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
                        return f"Aucune modification effectuée pour l'avis du film {avis.id_film} par {avis.utilisateur}."
                        return False

                    connection.commit()
                    print(f"Avis modifié avec succès pour le film {avis.id_film} par l'utilisateur {avis.utilisateur}.")
                    return True

        except Exception as e:
            print(f"Erreur lors de la modification de l'avis : {e}")
        return False

    def supprimer_avis(self,  utilisateur: str, id_film: int) -> bool:
        try: 
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Suppression de l'avis
                    cursor.execute(
                        "DELETE FROM avis WHERE  id_film = %s AND utilisateur = %s;",
                        (id_film, utilisateur),
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
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    query = "SELECT a.id, a.id_film, a.utilisateur, a.note, a.commentaire FROM avis a "
                    conditions = []
                    params = []

                    if id_film is not None:
                        conditions.append("a.id_film = %s")
                        params.append(id_film)

                    if utilisateur is not None:
                        conditions.append("a.utilisateur = %s")
                        params.append(utilisateur)

                    if id_utilisateur is not None:
                        query += "JOIN utilisateur u ON u.pseudo = a.utilisateur "
                        conditions.append("u.id_utilisateur = %s")
                        params.append(id_utilisateur)
            
                    if conditions:
                        query += " WHERE " + " AND ".join(conditions)
            
                    cursor.execute(query, tuple(params))
                    result = cursor.fetchall()
                    if not result:
                        return []

                    
                    return result

        except Exception as e:
            print(f"Erreur lors de la lecture des avis : {e}")
            return []  # Retourner une liste vide en cas d'erreur
