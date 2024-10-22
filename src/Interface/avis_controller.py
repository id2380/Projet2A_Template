from typing import TYPE_CHECKING, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Model.api_utilisateur import APIUtilisateur
from src.Model.utilisateur import Utilisateur
from src.Model.jwt_response import JWTResponse
from src.Interface.init_app import jwt_service, utilisateur_service, utilisateur_dao
from src.Interface.jwt_bearer import JWTBearer
from src.Service.mot_de_passe_service import valider_nom_utilisateur_mot_de_passe
from pydantic import BaseModel

if TYPE_CHECKING: # Soukayna, la classe Avis sera à rajouter dans les modèles
    from src.Model.avis import Avis

user_router = APIRouter(prefix="/avis", tags=["Avis"])

class RequeteCreationAvis(BaseModel):
    film: str
    utilisateur: str
    commentaire: str
    note: int

@app.post("/creer_avis", status_code=status.HTTP_201_CREATED)
    def creer_avis(requete: RequeteCreationAvis):
        try:
            avis = avis_service.ajouter_avis(
                id= None,
                film=requete.film,
                utilisateur=requete.utilisateur,
                note=requete.note,
                commentaire=requete.commentaire   
            )
            # Vérification si l'avis a été créé avec succès
            if avis :
                return {"message": "Votre avis a été créé avec succès."}
            else:
                raise ValueError("La création de l'avis a échoué.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erreur : {str(e)}")