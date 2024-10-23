from src.business_object.utilisateur import Utilisateur
# from src.service.utilisateur_service import UtilisateurService
# importer IDENTIFIANT 
from src.dao.utilisateur_dao import UtilisateurDAO
from src.data.db_connection import DBConnection
from src.utils.singleton import Singleton


class EclaireurDAO(metaclass=Singleton): 
    """Classe contenant les méthodes pour ajouter,
    accéder et gérer les éclaireurs de chaque utilisateur dans la bdd"""
    def __init__(self, id_utilisateur):
        self.id_utilisateur = id_utilisateur

    def ajouter_eclaireur(self, pseudo_eclaireur: str):
        """Création d'un couple utilisateur / éclaireur dans la bdd.
        Récupération de l'id de l'éclaireur souhaité  à partir de son pseudo,
        récupération AUTOMATIQUE de l'id de l'utilisateur connecté,
        puis ajout dans la BDD abonne du couple de id.

        Parameters
        ----------
        pseudo : str
           Le pseudo de l'utilisateur à ajouter comme éclaireur

        Returns
        -------
        created : bool
           True si l'ajout a réussi, False sinon"""
        
        # Récupérer l'id_utilisateur à partir du pseudo
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_utilisateur FROM utilisateur 
                        WHERE pseudo = %(pseudo_eclaireur)s
                        """,
                        {'pseudo_eclaireur': pseudo_eclaireur}
                    )
                    id_eclaireur = cursor.fetchone()
                    print(self.id_utilisateur)
                    print(id_eclaireur["id_utilisateur"])

                    if id_eclaireur is None:
                        print("Utilisateur non trouvé.")
                        return False
        
        # Ajouter l'éclaireur en utilisant l'id_utilisateur récupéré
                    cursor.execute(
                        """
                        INSERT INTO abonne(id_utilisateur, id_eclaireur)
                        VALUES (%(id_utilisateur)s, %(id_eclaireur)s)
                        RETURNING id_utilisateur
                        """,
                        {'id_utilisateur': self.id_utilisateur,
                         'id_eclaireur': id_eclaireur["id_utilisateur"]}
                     )
                    res = cursor.fetchone()
                    print(f"Vous suivez désormais {pseudo_eclaireur}")
                    return True
            
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'éclaireur : {e}")
            return False


    def chercher_eclaireur_pseudo(self, pseudo_eclaireur : str): 
        """Recherche éclaireur par pseudo
        Parameters
        ----------
        pseudo : str
           Le pseudo de l'utilisateur à rechercher

        Returns
        -------
        created : bool
           False si le pseudo n'existe pas 
           True s'il existe, + infos sur l'éclaireur ?
        """
        # Récupérer l'id_utilisateur à partir du pseudo
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT pseudo, film FROM avis 
                        JOIN utilisateur USING id_utilisateur
                        WHERE pseudo = %(pseudo_eclaireur)s
                        """,
                        {'pseudo_eclaireur': pseudo_eclaireur}
                    )
                    id_eclaireur = cursor.fetchone()
                    
                    if id_eclaireur is None:
                        print("Utilisateur non trouvé.")
                        return False
        
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'éclaireur : {e}")
            return False
        pass

    def supprimer_eclaireur(self, pseudo_eclaireur : str):
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_utilisateur FROM utilisateur 
                        WHERE pseudo = %(pseudo_eclaireur)s
                        """,
                        {'pseudo_eclaireur': pseudo_eclaireur}
                    )
                    id_eclaireur = cursor.fetchone()
                    print(self.id_utilisateur)
                    print(id_eclaireur["id_utilisateur"])

                    if id_eclaireur is None:
                        print("Utilisateur non trouvé.")
                        return False

                     # supprimer le couple utilisateur/éclaireur
                    cursor.execute(
                        """
                        DELETE FROM abonne
                        WHERE (id_eclaireur = %(id_eclaireur)s
                        AND id_utilisateur = %(id_utilisateur)s)
                        """,
                        {'id_utilisateur': self.id_utilisateur,
                         'id_eclaireur': id_eclaireur["id_utilisateur"]}
                     )
                    res = cursor.fetchone()

                    if res is None:
                        print("Vous n'êtes pas abonné.e à cet utilisateur")
                        return False
                    return True
            
        except Exception as e:
            print(f"Erreur lors de la suppression de l'éclaireur : {e}")
            return False

#test ajout eclaireur existant
if __name__ == "__main__":
    utilisateur = Utilisateur(6, "gab_utilisateur", mot_de_passe = "")
    utilisateurdao = EclaireurDAO(id_utilisateur = 4)
    print(utilisateurdao.ajouter_eclaireur("poupou1"))
        
#test ajout eclairuer non existant

#test ajout éclaireur qu'on suit déjà/erreur

#test supprimer eclaireur existant
if __name__ == "__main__":
    print(utilisateurdao.supprimer_eclaireur("tib_utilisateur"))


#test supprimer eclaireur non existant

#test supprimer eclaireur auquel on n'est pas abonnés