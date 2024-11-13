from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from src.Interface.jwt_bearer import JWTBearer
from src.Interface.user_controller import \
    obtenir_utilisateur_depuis_credentials
from src.service.avis_service import AvisService


class AvisRequest(BaseModel):
    id_film: int
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
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    result = avis_service.ajouter_avis(avis.id_film, utilisateur.pseudo, avis.commentaire,avis.note)
    if result:
        return f"Votre avis a bien été ajouter au film {avis.id_film} "

    else:
        raise HTTPException(status_code=400, detail="La création de l'avis a échoué.")

@avis_router.put("/{id_avis}", status_code=status.HTTP_200_OK)
def modifier_avis(id_avis: int, avis: AvisRequest, credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    avis_service = AvisService()
    if avis_service.modifier_avis(avis.id_film, utilisateur.pseudo, avis.commentaire, avis.note):
        return f"Votre avis a bien été modifier"
    else:
        raise HTTPException(status_code=404, detail="La modification de l'avis a échoué.")


@avis_router.delete("/{id_avis}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_avis( id_film :int , credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    avis_service = AvisService()
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    if avis_service.supprimer_avis(id_film, utilisateur.pseudo):
        return Response(content="Avis supprimé avec succès", status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=404, detail="La suppression de l'avis a échoué.")

@avis_router.get("/avis/", status_code=status.HTTP_200_OK)
def get_avis(
    id_film: Optional[int] = Query(None, description="L'identifiant du film pour lequel rechercher des avis"),
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    if not (id_film or utilisateur.pseudo ):
        raise HTTPException(status_code=400, detail="Au moins un paramètre parmi 'id_film', 'utilisateur' ou 'id_utilisateur' doit être fourni.")
    avis_service = AvisService()
    avis = avis_service.obtenir_avis(id_film=id_film, utilisateur=utilisateur.pseudo, id_utilisateur=None)
    if avis:
        if avis !=[] : 
            return f" Voici la liste des avis {avis}"
        return "Il n'y a pas d'avis pour les informations souhaitées "
    else:
        raise HTTPException(status_code=404, detail="Aucun avis trouvé pour les critères fournis.")

