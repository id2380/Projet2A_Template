from fastapi import APIRouter, HTTPException, status, Query, Depends
from src.service.avis_service import AvisService
from pydantic import BaseModel
from src.Interface.jwt_bearer import JWTBearer
from fastapi.security import HTTPAuthorizationCredentials

class AvisRequest(BaseModel):
    id_film: int
    utilisateur: str
    commentaire: str
    note: int

class AvisResponse(BaseModel):
    id_avis: int
    id_film: int
    utilisateur: str
    commentaire: str
    note: int

avis_router = APIRouter(prefix="/avis", tags=["Avis"])

@avis_router.post("/", response_model=AvisResponse, status_code=status.HTTP_201_CREATED)
def creer_avis(avis: AvisRequest, credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    avis_service = AvisService()
    result = avis_service.ajouter_avis(avis.id_film, avis.utilisateur, avis.commentaire, avis.note)
    if result:
        return result
    else:
        raise HTTPException(status_code=400, detail="La création de l'avis a échoué.")

@avis_router.put("/{id_avis}", response_model=AvisResponse, status_code=status.HTTP_200_OK)
def modifier_avis(id_avis: int, avis: AvisRequest, credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    avis_service = AvisService()
    if avis_service.modifier_avis(avis.id_film, avis.utilisateur, avis.commentaire, avis.note):
        return avis
    else:
        raise HTTPException(status_code=404, detail="La modification de l'avis a échoué.")

@avis_router.delete("/{id_avis}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_avis(id_avis: int, utilisateur: str, credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    avis_service = AvisService()
    if avis_service.supprimer_avis(id_avis, utilisateur):
        return {"message": "Avis supprimé avec succès"}
    else:
        raise HTTPException(status_code=404, detail="La suppression de l'avis a échoué.")

@avis_router.get("/film/{id_film}", response_model=list[AvisResponse], status_code=status.HTTP_200_OK)
def get_avis_par_film(id_film: int, credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    avis_service = AvisService()
    avis = avis_service.obtenir_avis_par_film(id_film)
    if avis:
        return avis
    else:
        raise HTTPException(status_code=404, detail="Aucun avis trouvé pour ce film.")

@avis_router.get("/utilisateur/", response_model=list[AvisResponse], status_code=status.HTTP_200_OK)
def get_avis_par_utilisateur(utilisateur: str = Query(None, alias="username"), credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    avis_service = AvisService()
    avis = avis_service.obtenir_avis_par_utilisateur(utilisateur)
    if avis:
        return avis
    else:
        raise HTTPException(status_code=404, detail="Aucun avis trouvé pour cet utilisateur.")
