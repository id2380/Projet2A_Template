from src.Model.utilisateur import Utilisateur
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
                        INSERT INTO utilisateur(pseudo, adresse_email, mot_de_passe, sel)
                        VALUES (%(pseudo)s, %(adresse_email)s, %(mot_de_passe)s, %(sel)s)
                        RETURNING id_utilisateur, date_creation;
                        """,
                        {
                            "pseudo": utilisateur.pseudo,
                            "adresse_email": utilisateur.adresse_email,
                            "mot_de_passe": utilisateur.mot_de_passe,  # Le mot de passe est déjà hashé
                            "sel": utilisateur.sel,
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

    def chercher_utilisateur_par_id(self, id_utilisateur: int) -> Utilisateur | None:
        """Cherche un utilisateur par son identifiant

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant de l'utilisateur à rechercher

        Returns
        -------
        Utilisateur ou None
            L'utilisateur correspondant ou None s'il n'existe pas
        """
        utilisateur = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM utilisateur
                        WHERE id_utilisateur = %(id_utilisateur)s;
                        """,
                        {"id_utilisateur": id_utilisateur}
                    )
                    res = cursor.fetchone()
                    if res:
                        utilisateur = Utilisateur(**res)
        except Exception as e:
            print(f"Erreur lors de la recherche de l'utilisateur par ID : {e}")
        return utilisateur

    def chercher_utilisateur_par_pseudo(self, pseudo: str) -> Utilisateur | None:
        """Cherche un utilisateur par son pseudo

        Parameters
        ----------
        pseudo : str
            Le pseudo de l'utilisateur à rechercher

        Returns
        -------
        Utilisateur ou None
            L'utilisateur correspondant ou None s'il n'existe pas
        """
        utilisateur = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM utilisateur
                        WHERE pseudo = %(pseudo)s;
                        """,
                        {"pseudo": pseudo}
                    )
                    res = cursor.fetchone()
                    if res:
                        utilisateur = Utilisateur(**res)
        except Exception as e:
            print(f"Erreur lors de la recherche de l'utilisateur par pseudo : {e}")
        return utilisateur
