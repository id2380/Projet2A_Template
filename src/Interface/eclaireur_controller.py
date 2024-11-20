from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Interface.jwt_bearer import JWTBearer
from src.Interface.user_controller import \
    obtenir_utilisateur_depuis_credentials
from src.service.eclaireur_service import EclaireurService

eclaireur_router = APIRouter(prefix="/Eclaireurs", tags=["Eclaireurs"])


@eclaireur_router.post("/ajouter_eclaireur_id", status_code=status.HTTP_200_OK)
def ajouter_eclaireur_id(
    id_eclaireur: int = Query(..., description="L'identifiant du futur éclaireur."),
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    "Permet d'ajouter, avec son id, un utilisateur à la liste de ses éclaireurs."
    import dotenv
    dotenv.load_dotenv(override=True)
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    try:
        EclaireurService().ajouter_eclaireur_id(utilisateur.id_utilisateur,
                                                id_eclaireur)
        return f"{id_eclaireur} fait maintenant partie de vos éclaireurs"
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@eclaireur_router.post("/ajouter_eclaireur_pseudo", status_code=201)
def ajouter_eclaireur_pseudo(
    pseudo_eclaireur: str = Query(..., description="Le pseudo du futur éclaireur."),
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    "Permet d'ajouter, avec son pseudo, un utilisateur à la liste de ses éclaireurs."
    import dotenv
    dotenv.load_dotenv(override=True)
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    try:
        EclaireurService().ajouter_eclaireur_pseudo(utilisateur.id_utilisateur,
                                                    pseudo_eclaireur)
        return f"{pseudo_eclaireur} fait maintenant partie de vos éclaireurs"
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@eclaireur_router.get("/est_eclaireur_id", status_code=201)
def est_eclaireur_id(
    id_eclaireur: int = Query(..., description="L'identifiant de l'utilisateur."),
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    "Permet de savoir, avec son id, si un utilisateur est dans sa liste d'éclaireurs."
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        if EclaireurService().est_eclaireur_id(utilisateur.id_utilisateur,
                                               id_eclaireur):
            return f"{id_eclaireur} fait partie de vos éclaireurs"
        else:
            return f"{id_eclaireur} ne fait pas partie de vos éclaireurs"
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@eclaireur_router.get("/est_eclaireur_pseudo", status_code=status.HTTP_200_OK)
def est_eclaireur_pseudo(
    pseudo_eclaireur: str = Query(..., description="Le pseudo du futur éclaireur."),
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    "Permet de savoir, avec son pseudo, si un utilisateur est dans sa liste d'éclaireurs."
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        if EclaireurService().est_eclaireur_pseudo(
            utilisateur.id_utilisateur,
            pseudo_eclaireur
        ):
            return f"{pseudo_eclaireur} fait partie de vos éclaireurs"
        else:
            return f"{pseudo_eclaireur} ne fait pas partie de vos éclaireurs"
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@eclaireur_router.get("/liste_eclaireurs", status_code=status.HTTP_200_OK)
def liste_eclaireurs(
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    "Permet d'obtenir la liste de ses éclaireurs."
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        eclaireurs = EclaireurService().liste_eclaireurs(
            utilisateur.id_utilisateur)
        return eclaireurs
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@eclaireur_router.delete("/supprimer_eclaireur_id", status_code=status.HTTP_200_OK)
def supprimer_eclaireur_id(
    id_eclaireur: int = Query(..., description="L'identifiant de l'éclaireur."),
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    "Permet de supprimer, avec son id, un utilisateur de sa liste d'éclaireurs."
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        EclaireurService().supprimer_eclaireur_id(
            utilisateur.id_utilisateur,
            id_eclaireur)
        return f"{id_eclaireur} ne fait plus partie de vos éclaireurs"
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@eclaireur_router.delete("/supprimer_eclaireur_pseudo", status_code=status.HTTP_200_OK)
def supprimer_eclaireur_pseudo(
    pseudo_eclaireur: str = Query(..., description="Le pseudo de l'éclaireur."),
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    "Permet de supprimer, avec son pseudo, un utilisateur de sa liste d'éclaireurs."
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        EclaireurService().supprimer_eclaireur_pseudo(
            utilisateur.id_utilisateur,
            pseudo_eclaireur)
        return f"{pseudo_eclaireur} ne fait plus partie de vos éclaireurs"
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")
