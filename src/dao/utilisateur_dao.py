from src.business_object.utilisateur import Utilisateur
from src.data.db_connection import DBConnection


class UtilisateurDAO:
    """Classe contenant les méthodes pour créer,
    accéder et gérer les utilisateurs dans la base de données"""

    def creer(self, utilisateur: Utilisateur) -> bool:
        """Création d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur
            L'utilisateur à créer

        Returns
        -------
        created : bool
            True si la création a réussi, False sinon
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO utilisateur(pseudo, adresse_email, mot_de_passe)
                        VALUES (%(pseudo)s, %(adresse_email)s, %(mot_de_passe)s)
                        RETURNING id_utilisateur, date_creation;
                        """,
                        {
                            "pseudo": utilisateur.pseudo,
                            "adresse_email": utilisateur.adresse_email,
                            "mot_de_passe": utilisateur.mot_de_passe,  # Le mot de passe est déjà hashé
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            print(f"Erreur lors de la création de l'utilisateur : {e}")
            return False

        # Si l'insertion est réussie, récupérer l'identifiant et la date de création
        if res:
            utilisateur.id_utilisateur = res["id_utilisateur"] 
            utilisateur.date_creation = res["date_creation"] 
            print(f"Utilisateur {utilisateur.pseudo} créé avec succès dans la base.")
            return True
        return False
