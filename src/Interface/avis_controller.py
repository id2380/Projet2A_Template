from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

from src.dao.eclaireur_dao import EclaireurDAO
from src.Interface.jwt_bearer import JWTBearer
from src.Interface.user_controller import \
    obtenir_utilisateur_depuis_credentials
from src.service.avis_service import AvisService

avis_router = APIRouter(prefix="/avis", tags=["Avis"])


@avis_router.post("/ajouter_avis", status_code=status.HTTP_200_OK)
def ajouter_avis(
    id_film: int= Query(..., description="L'identifiant du film pour lequel l'avis est ajouté."),
    note: int = Query(..., description="La note attribuée au film (entre 0 et 10)."),
    commentaire: str = Query(None, description="Un commentaire facultatif sur le film."),
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    """Ajoute un avis pour un film spécifique avec une note sur 10 et un commentaire optionnel."""
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
    id_film: int= Query(..., description="L'identifiant du film pour lequel l'avis est modifié."),
    note: int= Query(..., description="La nouvelle note attribuée au film (entre 0 et 10)."),
    commentaire: str =Query(None, description="Un commentaire facultatif modifié pour l'avis."),
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    """
    Modifie un avis donné pour un film.
    """
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
    id_film: int = Query(..., description="L'identifiant du film pour lequel l'avis est supprimé."),
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    """
    Supprime un avis pour un film.
    """
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
    id_film: int = Query(None, description="L'identifiant du film pour lequel les avis sont recherchés."),
    id_utilisateur: int = Query(None, description="L'identifiant de l'utilisateur dont les avis sont recherchés."),
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    """
    Recherche des avis selon les critères si pas de critères renvoie la liste des avis de l'utilisateur.
    """
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
    id_film: int = Query(..., description="L'identifiant du film pour lequel les avis sont recherchés."),
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    """Recherche les avis partagés par mes éclaireurs pour un film donné"""
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
    id_utilisateur: int= Query(..., description="L'identifiant de l'éclaireur."),
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    """Recherche les avis partagés entre moi et un éclaireur pour un même film."""
    import dotenv
    dotenv.load_dotenv(override=True)
    avis_service = AvisService()
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    id_utilisateur1 = utilisateur.id_utilisateur
    if not EclaireurDAO().est_eclaireur(id_utilisateur1,id_utilisateur):
        return "L'identifiant entré ne fait pas partie de vos éclaireurs"
    try:
        return avis_service.lire_avis_communs(id_utilisateur1, id_utilisateur)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@avis_router.get("/note_moyenne", status_code=status.HTTP_200_OK)
def calculer_note_moyenne(
    id_film: int =Query(...,description="Identifiant du film pour lequel la note moyenne est calculée."),
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    """Calcule la note moyenne attribuée à un film par tous les utilisateurs."""
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        return AvisService().calculer_note_moyenne(id_film=id_film)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@avis_router.get("/note_moyenne_eclaireurs", status_code=status.HTTP_200_OK)
def calculer_note_moyenne_eclaireurs(
    id_film: int=Query(...,description="Identifiant du film pour lequel la note moyenne est calculée."),
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    """Calcule la note moyenne attribuée à un film par tous mes éclaireurs."""
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
