from typing import TYPE_CHECKING, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import HTTPAuthorizationCredentials
from src.Interface.init_app import jwt_service, utilisateur_service, utilisateur_dao
from src.Model.api_utilisateur import APIUtilisateur
from src.Model.utilisateur import Utilisateur
from src.Model.jwt_response import JWTResponse
from src.Interface.jwt_bearer import JWTBearer
from pydantic import BaseModel
from src.Service.film_service import FilmService
from src.Service.avis_service import AvisService
from src.dao.avis_dao import AvisDAO
if TYPE_CHECKING:
    from src.Model.avis import Avis

# Création du routeur pour l'API Avis
avis_router = APIRouter(prefix="/avis", tags=["Avis"])


@avis_router.get("/creer_avis", status_code=status.HTTP_201_CREATED)
def creer_avis(id_film: int, utilisateur: str, commentaire: str, note: int):
    import dotenv
    dotenv.load_dotenv(override=True)
    avis= None
    try:
        avis_service = AvisService()
        # Création de l'avis avec l'ID du film fourni par l'utilisateur
        avis = avis_service.ajouter_avis(
            id_film=id_film,  # Utilisation de l'ID du film fourni en paramètre
            utilisateur=utilisateur,
            note=note,
            commentaire=commentaire
        )

        # Vérification si l'avis a été créé avec succès
        if avis:
            return {"message": "Votre avis a été créé avec succès."}
        else:
            raise ValueError("La création de l'avis a échoué.")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la création de l'avis : {str(e)}")

@avis_router.get("/modifier_avis", status_code=status.HTTP_200_OK)
def modifier_avis(id_film: int, utilisateur: str, commentaire: str, note: int):
    import dotenv
    dotenv.load_dotenv(override=True)
    avis= None
    try:
        # Créez une instance d'AvisDAO
        avis_dao = AvisDAO()

        # Instanciez le service AvisService avec le DAO
        avis_service = AvisService(avis_dao)
        # Création de l'avis avec l'ID du film fourni par l'utilisateur
        avis = avis_service.ajouter_avis(
            id_film=id_film,  # Utilisation de l'ID du film fourni en paramètre
            utilisateur=utilisateur,
            note=note,
            commentaire=commentaire
        )

        # Vérification si l'avis a été créé avec succès
        if avis:
            return {"message": "Votre avis a été créé avec succès."}
        else:
            raise ValueError("La création de l'avis a échoué.")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la création de l'avis : {str(e)}")
