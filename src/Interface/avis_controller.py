from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

from src.Interface.jwt_bearer import JWTBearer
from src.Interface.user_controller import \
    obtenir_utilisateur_depuis_credentials
from src.service.avis_service import AvisService

avis_router = APIRouter(prefix="/avis", tags=["Avis"])


@avis_router.post("/ajouter_avis", status_code=status.HTTP_200_OK)
def ajouter_avis(
    id_film: int,
    note: int,
    commentaire: str = None,
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    import dotenv
    dotenv.load_dotenv(override=True)
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    avis_service = AvisService()
    try:
        if note < 0 or note > 10:
            raise ValueError("La note doit être comprise entre 0 et 10.")
        avis_service.ajouter_avis(id_film=id_film,
                                  id_utilisateur=utilisateur.id_utilisateur,
                                  note=note,
                                  commentaire=commentaire)
        return f"Création réussite de votre avis pour l'id film : {id_film}"
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@avis_router.put("/modifier_avis", status_code=status.HTTP_200_OK)
def modifier_avis(
    id_film: int,
    note: int,
    commentaire: str = None,
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    import dotenv
    dotenv.load_dotenv(override=True)
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    avis_service = AvisService()
    try:
        if note < 0 or note > 10:
            raise ValueError("La note doit être comprise entre 0 et 10.")
        avis_service.modifier_avis(id_film=id_film,
                                   id_utilisateur=utilisateur.id_utilisateur,
                                   note=note,
                                   commentaire=commentaire)
        return f"Modification réussite de votre avis pour l'id film : {id_film}"
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@avis_router.delete("/supprimer_avis", status_code=status.HTTP_200_OK)
def supprimer_avis(
    id_film: int,
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    import dotenv
    dotenv.load_dotenv(override=True)
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    avis_service = AvisService()
    try:
        avis_service.supprimer_avis(id_film=id_film,
                                    id_utilisateur=utilisateur.id_utilisateur)
        return f"Suppression réussite de votre avis pour l'id film : {id_film}"
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@avis_router.get("/rechercher_avis", status_code=status.HTTP_200_OK)
def recherche_avis(
    id_film: int = None,
    id_utilisateur: int = None,
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    import dotenv
    dotenv.load_dotenv(override=True)
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    avis_service = AvisService()
    if id_film is None and id_utilisateur is None:
        try:
            return avis_service.obtenir_avis(
                id_utilisateur=utilisateur.id_utilisateur
                )
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")
    else:
        try:
            return avis_service.obtenir_avis(id_film=id_film,
                                             id_utilisateur=id_utilisateur)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@avis_router.get("/rechercher_avis_eclaireurs", status_code=status.HTTP_200_OK)
def recherche_avis_eclaireurs(
    id_film: int,
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    import dotenv
    dotenv.load_dotenv(override=True)
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    avis_service = AvisService()
    try:
        return avis_service.lire_avis_eclaireurs(
            id_film=id_film,
            id_utilisateur=utilisateur.id_utilisateur
            )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@avis_router.get("/films_communs", status_code=status.HTTP_200_OK)
def recherche_films_communs(
    id_utilisateur1: int,
    id_utilisateur2: int,
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    import dotenv
    dotenv.load_dotenv(override=True)
    avis_service = AvisService()
    try:
        return avis_service.lire_avis_communs(id_utilisateur1, id_utilisateur2)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@avis_router.get("/note_moyenne", status_code=status.HTTP_200_OK)
def calculer_note_moyenne(
    id_film: int,
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        return AvisService().calculer_note_moyenne(id_film=id_film)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@avis_router.get("/note_moyenne_eclaireurs", status_code=status.HTTP_200_OK)
def calculer_note_moyenne_eclaireurs(
    id_film: int,
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    import dotenv
    dotenv.load_dotenv(override=True)
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)                               
    try:
        return AvisService().calculer_note_moyenne_eclaireurs(
            id_film=id_film,
            id_utilisateur=utilisateur.id_utilisateur
            )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")
