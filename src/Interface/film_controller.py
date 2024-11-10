from typing import TYPE_CHECKING, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Model.api_utilisateur import APIUtilisateur
from src.Model.utilisateur import Utilisateur
from src.Model.jwt_response import JWTResponse
from src.Interface.init_app import jwt_service, utilisateur_service, utilisateur_dao
from src.Interface.jwt_bearer import JWTBearer
from pydantic import BaseModel
from src.service.film_service import FilmService
from src.service.avis_service import AvisService

if TYPE_CHECKING:
    from src.Model.Movie import Movie

film_router = APIRouter(prefix="/films", tags=["Films"])


@film_router.get("/recherche_films", status_code=status.HTTP_200_OK)
def recherche_films(title: str = None, language: str = "en-US", primary_release_year: int = None, year: int = None):
    import dotenv

    dotenv.load_dotenv(override=True)
    films = None
    try:
        films = FilmService().recherche_films(
            title=title, language=language, primary_release_year=primary_release_year, year=year
        )
        # Vérification si l'avis a été créé avec succès
        if films is None:
            raise ValueError("Aucun film ne correspond à vos critères")
        return films
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@film_router.get("/recherche_films_similaires", status_code=status.HTTP_200_OK)
def recherche_films_similaires(id_film: int):
    import dotenv

    dotenv.load_dotenv(override=True)
    films = None
    try:
        films = FilmService().recherche_films_similaires(id_film)
        # Vérification si l'avis a été créé avec succès
        if films is None:
            raise ValueError("Aucun film ne correspond à vos critères")
        return films
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@film_router.get("/fiche_technique", status_code=status.HTTP_200_OK)
def obtenir_fiche_technique(id_film: int):
    import dotenv

    dotenv.load_dotenv(override=True)
    try:
        film = FilmService().obtenir_film_complet(id_film)
        if film is None:
            raise ValueError("Aucun film ne correspond à l'ID")
        """
        avis_service = AvisService()
        film.fiche_technique.note_moyenne = avis_service.calculer_note_moyenne(id_film)
        film.fiche_technique.avis = avis_service.obtenir_avis_par_film(id_film)
        """
        return film
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")
