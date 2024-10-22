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

if TYPE_CHECKING:
    from src.Model.Movie import Movie

user_router = APIRouter(prefix="/films", tags=["Films"])

@user_router.get("/recherche_films", status_code=status.HTTP_200_OK)
def recherche_films(title: str = None,
                    language: str = "en-US",
                    primary_release_year: int = None,
                    year: int = None):
    import dotenv
    dotenv.load_dotenv(override=True)
    films = None
    try:
        films = FilmService().recherche_films(title=title,
                                                language = language,
                                                primary_release_year = primary_release_year,
                                                year = year)
        # Vérification si l'avis a été créé avec succès
        if films is None:
            raise ValueError("Aucun film ne correspond à vos critères")
        return films
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")