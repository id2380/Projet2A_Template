from src.business_object.avis import Avis
from src.business_object.film import Film
from src.business_object.utilisateur import Utilisateur
from src.data.db_connection import DBConnection

class AvisDAO:

    """Classe contenant les méthodes pour créer, consulter, modifier et supprimer des avis dans la base de données."""

    def creer_avis(self, avis: Avis) -> bool:
        """Création d'un avis dans la base de données."""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # D'abord, récupérer l'id de l'utilisateur depuis le pseudo
                    cursor.execute("SELECT id_utilisateur FROM utilisateur WHERE pseudo = %s;", (avis.utilisateur,))
                    id_utilisateur = cursor.fetchone()
                    if id_utilisateur is None:
                        raise ValueError(f"L'utilisateur {avis.utilisateur} n'existe pas.")

                    # Ensuite, récupérer l'id du film depuis le titre
                    cursor.execute("SELECT id_film FROM film WHERE titre = %s;", (avis.film,))
                    id_film = cursor.fetchone()
                    if id_film is None:
                        raise ValueError(f"Le film {avis.film} n'existe pas.")

                    # Insérer l'avis avec les id_utilisateur et id_film
                    cursor.execute(
                        """
                        INSERT INTO avis(film, utilisateur, note, commentaire, id_utilisateur, id_film)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING id;
                        """,
                        (avis.film, avis.utilisateur, avis.note, avis.commentaire, id_utilisateur[0], id_film[0])
                    )
                    avis.id = cursor.fetchone()[0]  # Récupération de l'ID généré
                    connection.commit()
            print(f"Avis créé avec succès dans la base.")
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
