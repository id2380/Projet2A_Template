from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.dao.utilisateur_dao import UtilisateurDAO
from src.Interface.jwt_bearer import JWTBearer
from src.Interface.user_controller import \
    obtenir_utilisateur_depuis_credentials
from src.Service.eclaireurs_service import EclaireurService

eclaireurs_router = APIRouter(prefix="/Eclaireurs", tags=["Eclaireurs"])


@eclaireurs_router.get("/ajouter_eclaireur_id", status_code=status.HTTP_200_OK)
def ajouter_eclaireur_id(id_eclaireur: int,
                         credentials: HTTPAuthorizationCredentials = 
                         Depends(JWTBearer())):
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        EclaireurService().ajouter_eclaireur_id(utilisateur.id_utilisateur,
                                                id_eclaireur, True)
        print(f"{id_eclaireur} fait maintenant partie de vos éclaireurs")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@eclaireurs_router.get("/ajouter_eclaireur_pseudo",
                       status_code=status.HTTP_200_OK)
def ajouter_eclaireur_pseudo(pseudo_eclaireur: str,
                             credentials: HTTPAuthorizationCredentials =
                             Depends(JWTBearer())):
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        EclaireurService().ajouter_eclaireur_pseudo(utilisateur.id_utilisateur,
                                                    pseudo_eclaireur)
        print(f"{pseudo_eclaireur} fait maintenant partie de vos éclaireurs")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@eclaireurs_router.get("/est_eclaireur_id", status_code=status.HTTP_200_OK)
def est_eclaireur_id(id_eclaireur: int,
                     credentials: HTTPAuthorizationCredentials =
                     Depends(JWTBearer())):
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        if EclaireurService().est_eclaireur_id(utilisateur.id_utilisateur,
                                               id_eclaireur):
            print(f"{id_eclaireur} fait partie de vos éclaireurs")
        else:
            print(f"{id_eclaireur} ne fait pas partie de vos éclaireurs")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@eclaireurs_router.get("/est_eclaireur_pseudo", status_code=status.HTTP_200_OK)
def est_eclaireur_pseudo(pseudo_eclaireur: str,
                         credentials: HTTPAuthorizationCredentials =
                         Depends(JWTBearer())):
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        if EclaireurService().est_eclaireur_pseudo(utilisateur.id_utilisateur,
                                                   pseudo_eclaireur):
            print(f"{pseudo_eclaireur} fait partie de vos éclaireurs")
        else:
            print(f"{pseudo_eclaireur} ne fait pas partie de vos éclaireurs")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@eclaireurs_router.get("/supprimer_eclaireur_id",
                       status_code=status.HTTP_200_OK)
def supprimer_eclaireur_id(id_eclaireur: int,
                           credentials: HTTPAuthorizationCredentials =
                           Depends(JWTBearer())):
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        EclaireurService().supprimer_eclaireur_id(utilisateur.id_utilisateur,
                                                  id_eclaireur)
        print(f"{id_eclaireur} ne fait plus partie de vos éclaireurs")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@eclaireurs_router.get("/supprimer_eclaireur_pseudo",
                       status_code=status.HTTP_200_OK)
def supprimer_eclaireur_pseudo(pseudo_eclaireur: str,
                               credentials: HTTPAuthorizationCredentials =
                               Depends(JWTBearer())):
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        EclaireurService().supprimer_eclaireur_pseudo(utilisateur.id_utilisateur,
                                                      pseudo_eclaireur)
        print(f"{pseudo_eclaireur} ne fait plus partie de vos éclaireurs")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@eclaireurs_router.get("/liste_eclaireurs", status_code=status.HTTP_200_OK)
def liste_eclaireurs(credentials: HTTPAuthorizationCredentials =
                     Depends(JWTBearer())):
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        eclaireurs = EclaireurService().liste_eclaireurs(utilisateur.id_utilisateur)
        return eclaireurs
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")