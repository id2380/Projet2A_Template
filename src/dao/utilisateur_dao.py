from src.data.db_connection import DBConnection
from src.Model.utilisateur import Utilisateur


class UtilisateurDAO:
    """
    Classe contenant les méthodes pour créer, accéder et gérer les
    utilisateurs dans la base de données.
    """

    def creer(self, utilisateur: Utilisateur) -> bool:
        """
        Création d'un utilisateur dans la base de données.

        Note: Le mot de passe doit être déjà haché avant d'appeler cette
              méthode. C'est fait dans la classe de service.

        Parameters
        ----------
        utilisateur : Utilisateur
            L'utilisateur à créer.

        Returns
        -------
        bool
            True si la création a réussi, False sinon.

        Exception
        -------
        ValueError : erreur lors de la création de l'utilisateur dans la base.
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO utilisateur(pseudo, adresse_email,
                        mot_de_passe, sel) VALUES (%(pseudo)s,
                        %(adresse_email)s, %(mot_de_passe)s, %(sel)s)
                        RETURNING id_utilisateur, date_creation;
                        """,
                        {
                            "pseudo": utilisateur.pseudo,
                            "adresse_email": utilisateur.adresse_email,
                            "mot_de_passe": utilisateur.mot_de_passe,
                            "sel": utilisateur.sel,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            print(f"Erreur lors de la création de l'utilisateur : {e}")
            return False

        # Si l'insertion est réussie, récupérer l'identifiant et la date de
        # création
        if res:
            utilisateur.id_utilisateur = res["id_utilisateur"]
            utilisateur.date_creation = res["date_creation"]
            print(
                f"Utilisateur {utilisateur.pseudo} créé avec succès dans la base."
            )
            return True
        return False

    def chercher_utilisateur_par_id(
        self, id_utilisateur: int
    ) -> Utilisateur | None:
        """
        Cherche un utilisateur par son identifiant.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant de l'utilisateur à rechercher.

        Returns
        -------
        Utilisateur ou None
            L'utilisateur correspondant ou None s'il n'existe pas.

        Exception
        -------
        ValueError : erreur lors de la recherche dans la base.
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
                        {"id_utilisateur": id_utilisateur},
                    )
                    res = cursor.fetchone()
                    if res:
                        utilisateur = Utilisateur(**res)
        except Exception as e:
            print(f"Erreur lors de la recherche de l'utilisateur par ID : {e}")
        return utilisateur

    def chercher_utilisateur_par_pseudo(
        self, pseudo: str
    ) -> Utilisateur | None:
        """
        Cherche un utilisateur par son pseudo.

        Parameters
        ----------
        pseudo : str
            Le pseudo de l'utilisateur à rechercher.

        Returns
        -------
        Utilisateur ou None
            L'utilisateur correspondant ou None s'il n'existe pas.
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
                        {"pseudo": pseudo},
                    )
                    res = cursor.fetchone()
                    if res:
                        utilisateur = Utilisateur(**res)
        except Exception as e:
            print(
                f"Erreur lors de la recherche de l'utilisateur par pseudo : {e}"
            )
        return utilisateur

    def modifier_pseudo(
        self, id_utilisateur: int, nouveau_pseudo: str
    ) -> bool:
        """
        Modifie le pseudo d'un utilisateur.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant de l'utilisateur dont le pseudo doit être modifié.
        nouveau_pseudo : str
            Le nouveau pseudo à définir pour l'utilisateur.

        Returns
        -------
        bool
            True si la modification a réussi, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE utilisateur
                        SET pseudo = %(pseudo)s
                        WHERE id_utilisateur = %(id_utilisateur)s;
                        """,
                        {
                            "pseudo": nouveau_pseudo,
                            "id_utilisateur": id_utilisateur,
                        },
                    )
                    connection.commit()
                    return True
        except Exception as e:
            print(f"Erreur lors de la modification du pseudo : {e}")
            return False

    def modifier_adresse_email(
        self, id_utilisateur: int, nouvelle_adresse_email: str
    ) -> bool:
        """
        Modifie l'adresse e-mail d'un utilisateur.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant de l'utilisateur dont l'adresse e-mail doit être
            modifiée.
        nouvelle_adresse_email : str
            La nouvelle adresse e-mail à définir pour l'utilisateur.

        Returns
        -------
        bool
            True si la modification a réussi, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE utilisateur
                        SET adresse_email = %(adresse_email)s
                        WHERE id_utilisateur = %(id_utilisateur)s;
                        """,
                        {
                            "adresse_email": nouvelle_adresse_email,
                            "id_utilisateur": id_utilisateur,
                        },
                    )
                    connection.commit()
                    return True
        except Exception as e:
            print(f"Erreur lors de la modification de l'adresse e-mail : {e}")
            return False

    def modifier_mot_de_passe(
        self, id_utilisateur: int, nouveau_mot_de_passe: str
    ) -> bool:
        """
        Modifie le mot de passe d'un utilisateur.

        Note: Le mot de passe doit être déjà haché avant d'appeler cette
        méthode. C'est fait dans la classe de service.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant de l'utilisateur dont le mot de passe doit être
            modifié.
        nouveau_mot_de_passe : str
            Le nouveau mot de passe haché à définir pour l'utilisateur.

        Returns
        -------
        bool
            True si la modification a réussi, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE utilisateur
                        SET mot_de_passe = %(mot_de_passe)s
                        WHERE id_utilisateur = %(id_utilisateur)s;
                        """,
                        {
                            "mot_de_passe": nouveau_mot_de_passe,
                            "id_utilisateur": id_utilisateur,
                        },
                    )
                    connection.commit()
                    return True
        except Exception as e:
            print(f"Erreur lors de la modification du mot de passe : {e}")
            return False

    def supprimer_utilisateur(self, id_utilisateur: int) -> bool:
        """
        Supprime un utilisateur de la base de données.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant de l'utilisateur à supprimer.

        Returns
        -------
        bool
            True si la suppression a réussi, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM utilisateur
                        WHERE id_utilisateur = %(id_utilisateur)s;
                        """,
                        {"id_utilisateur": id_utilisateur},
                    )
                    connection.commit()
                    return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'utilisateur : {e}")
            return False

    def lister_tous_les_utilisateurs(self) -> list[Utilisateur]:
        """
        Liste tous les utilisateurs de la base de données.

        Returns
        -------
        list[Utilisateur]
            Liste de tous les utilisateurs.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM utilisateur;")
                    res = cursor.fetchall()
        except Exception as e:
            raise Exception(
                "Erreur lors de la récupération des utilisateurs"
            ) from e
        liste_utilisateurs = []
        if res:
            for row in res:
                utilisateur = Utilisateur(
                    id_utilisateur=row["id_utilisateur"],
                    pseudo=row["pseudo"],
                    adresse_email=row["adresse_email"],
                    mot_de_passe=row["mot_de_passe"],
                    date_creation=row["date_creation"],
                    sel=row["sel"],
                )
                liste_utilisateurs.append(utilisateur)

        return liste_utilisateurs

    def chercher_utilisateurs_par_pseudo_partiel(self, pseudo_partiel: str) -> list[Utilisateur]:
        """
        Cherche des utilisateurs dont le pseudo contient une chaîne partielle.

        Parameters
        ----------
        pseudo_partiel : str
            La chaîne partielle à rechercher dans les pseudos des utilisateurs.

        Returns
        -------
        list[Utilisateur]
            Liste des utilisateurs correspondant au critère ou une liste vide s'il n'y a pas de correspondance.
        """
        utilisateurs = []
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM utilisateur
                        WHERE pseudo ILIKE %(pseudo_partiel)s;
                        """,
                        {"pseudo_partiel": f"%{pseudo_partiel}%"},
                    )
                    res = cursor.fetchall()
                    if res:
                        utilisateurs = [Utilisateur(**row) for row in res]
        except Exception as e:
            print(f"Erreur lors de la recherche d'utilisateurs par pseudo partiel : {e}")
        return utilisateurs

