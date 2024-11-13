from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

from src.Interface.jwt_bearer import JWTBearer
from src.service.avis_service import AvisService


class AvisRequest(BaseModel):
    id_film: int
    utilisateur: str
    commentaire: str
    note: int
    


class AvisResponse(BaseModel):  # Modèle de réponse pour refléter les données retournées
    id_avis: int
    id_film: int
    utilisateur: str
    commentaire: str
    note: int


avis_router = APIRouter(prefix="/avis", tags=["Avis"])


@avis_router.post("/", status_code=status.HTTP_200_OK)
def creer_avis(avis: AvisRequest, credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    avis_service = AvisService()
    result = avis_service.ajouter_avis(avis.id_film, avis.utilisateur, avis.commentaire,avis.note)
    if result:
        return f"Votre avis a bien été ajouter au film {id_film }"

    else:
        raise HTTPException(status_code=400, detail="La création de l'avis a échoué.")

@avis_router.put("/{id_avis}", status_code=status.HTTP_200_OK)
def modifier_avis(id_avis: int, avis: AvisRequest, credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    avis_service = AvisService()
    if avis_service.modifier_avis(avis.id_film, avis.utilisateur, avis.commentaire, avis.note):
        return f"Votre avis a bien été modifier"
    else:
        raise HTTPException(status_code=404, detail="La modification de l'avis a échoué.")


@avis_router.delete("/{id_avis}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_avis(id_avis: int, utilisateur: str, credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    avis_service = AvisService()
    if avis_service.supprimer_avis(id_avis, utilisateur):
        return {"message": "Avis supprimé avec succès"}
    else:
        raise HTTPException(status_code=404, detail="La suppression de l'avis a échoué.")


@avis_router.get("/film/{id_film}",  status_code=status.HTTP_200_OK)
def get_avis_par_film(id_film: int, credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    avis_service = AvisService()
    avis = avis_service.obtenir_avis_par_film(id_film)
    if avis:
        return f"Voici la liste des avis pour le film {id_film } : "
        return avis
    else:
        raise HTTPException(status_code=404, detail="Aucun avis trouvé pour ce film.")


@avis_router.get("/utilisateur/",  status_code=status.HTTP_200_OK)
def get_avis_par_utilisateur(utilisateur: str = Query(None, alias="username"), credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    avis_service = AvisService()
    avis = avis_service.obtenir_avis_par_utilisateur_pseudo(utilisateur)
    if avis:
        return f"Voici la liste des avis pour l'utilisateur {utilisateur } : "
        return avis 
    else:
        raise HTTPException(status_code=404, detail="Aucun avis trouvé pour cet utilisateur.")
