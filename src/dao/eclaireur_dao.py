from src.Model.utilisateur import Utilisateur
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
        res = False
        eclaireur = UtilisateurDAO().chercher_utilisateur_par_pseudo(pseudo_eclaireur)
        if eclaireur is not None :
            try :
                # Ajouter l'éclaireur en utilisant l'id_utilisateur récupéré
                with DBConnection().connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """
                            INSERT INTO abonne(id_utilisateur, id_eclaireur)
                            VALUES (%(id_utilisateur)s, %(id_eclaireur)s)
                            RETURNING id_utilisateur
                            """,
                            {'id_utilisateur': self.id_utilisateur,
                                'id_eclaireur': eclaireur.id_utilisateur}
                        )
            except Exception as e:
                print(f"Erreur lors de l'ajout de l'éclaireur : {e}")
                return res
            print(f"Vous suivez maintenant : {eclaireur.pseudo}")
            return True

        print("Utilisateur non trouvé.")
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
        res = False
        eclaireur = UtilisateurDAO().chercher_utilisateur_par_pseudo(pseudo_eclaireur)
        if eclaireur is not None :
            try :
                # Ajouter l'éclaireur en utilisant l'id_utilisateur récupéré
                with DBConnection().connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """
                            SELECT *
                            FROM abonne
                            WHERE id_utilisateur = %(id_utilisateur)s AND id_eclaireur =%(id_eclaireur)s
                            """,
                            {'id_utilisateur': self.id_utilisateur,
                                'id_eclaireur': eclaireur.id_utilisateur}
                        )
                        return True
            except Exception as e:
                print(f"Erreur lors de la recherche de l'éclaireur : {e}")
        return False
            


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
                    
                    if cursor.rowcount == 0:
                        print("Aucun éclaireur trouvé. Vous n'êtes pas abonné.e à cet utilisateur.")
                        return False
                    elif cursor.rowcount == 1:
                        print(f"{pseudo_eclaireur} a été supprimé.e de la liste de vos éclaireurs.")
                        return True
                    else:
                        return False
            
        except Exception as e:
            print(f"Erreur lors de la suppression de l'éclaireur : {e}")
            return False

#test ajout eclaireur existant
if __name__ == "__main__":
    # Créer un utilisateur
    utilisateur = Utilisateur(pseudo="gob_utilisateur", adresse_email="",mot_de_passe = "",sel="")
    # Créer un éclaireur 
    eclaireur = Utilisateur(pseudo="tib_utilisateur", adresse_email="test", mot_de_passe = "",sel="")
    # Créer DAOs
    utilisateur_dao = UtilisateurDAO()
    # Créer utilisateur dans la base
    #utilisateur_dao.creer(utilisateur)
    #utilisateur_dao.creer(eclaireur)

    eclaireur_dao = EclaireurDAO(UtilisateurDAO().chercher_utilisateur_par_pseudo(utilisateur.pseudo).id_utilisateur)
    utilisateur_dao = UtilisateurDAO()
    

    # eclaireur_dao.ajouter_eclaireur(eclaireur.pseudo)
    print(eclaireur_dao.chercher_eclaireur_pseudo("test"))


    
    #print(utilisateurdao.ajouter_eclaireur("poupou1"))

"""      
#test ajout eclaireur non existant
if __name__ == "__main__":
    print(utilisateurdao.ajouter_eclaireur("pépé2"))

#test ajout éclaireur qu'on suit déjà/erreur

#test supprimer eclaireur existant
if __name__ == "__main__":
    print(utilisateurdao.supprimer_eclaireur("poupou1"))


#test supprimer eclaireur non existant

#test supprimer eclaireur auquel on n'est pas abonnés"""