from src.business_object.utilisateur import Utilisateur
from src.dao.utilisateur_dao import UtilisateurDAO
from src.data.db_connection import DBConnection

# importer IDENTIFIANT 

class EclaireurDAO : 
    """Classe contenant les méthodes pour ajouter,
    accéder et gérer les éclaireurs de chaque utilisateur dans la base de données"""

    def ajouter_eclaireur(self, pseudo : str):
        """Création d'un couple utilisateur / éclaireur dans la bdd
        
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
                        WHERE pseudo == %(pseudo)s
                        """,
                        {'pseudo': pseudo}
                    )
                    id_utilisateur = cursor.fetchone()
                    
                    if id_utilisateur is None: 
                        print("Utilisateur non trouvé.")
                        return False
        
        # Ajouter l'éclaireur en utilisant l'id_utilisateur récupéré
                    cursor.execute(
                        """
                        INSERT INTO abonne(id_utilisateur, id_eclaireur)
                        VALUES (utilisateur.id_utilisateur, %(id_utilisateur)s)
                        """,
                     )
                    res = cursor.fetchone()
            
            return True 
            
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'éclaireur : {e}")
            return False


    def chercher_eclaireur(self, pseudo : str): 
        pass

    def supprimer_eclaireur(self, pseudo : str):
        pass