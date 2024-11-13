from fastapi import APIRouter, Depends, HTTPException, status

from src.Interface.jwt_bearer import JWTBearer
from src.Interface.user_controller import \
    obtenir_utilisateur_depuis_credentials
from src.service.film_service import FilmService

film_router = APIRouter(prefix="/films", tags=["Films"])


@film_router.get("/recherche_films", status_code=status.HTTP_200_OK)
def recherche_films(titre: str = None,
                    language: str = "fr",
                    annee_de_sortie: int = None,
                    annee_de_production: int = None):
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        films = FilmService().recherche_films(title=titre,
                                              language=language,
                                              primary_release_year=annee_de_sortie,
                                              year=annee_de_production)
        return films
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@film_router.get("/recherche_films_similaires", status_code=status.HTTP_200_OK)
def recherche_films_similaires(id_film: int,
                               language: str = "fr"):
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        films = FilmService().recherche_films_similaires(id_film=id_film,
                                                         language=language)
        return films
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@film_router.get("/informations_techniques", status_code=status.HTTP_200_OK)
def obtenir_fiche_technique(id_film: int):
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        film = FilmService().recherche_film_id(id_film=id_film)
        return film
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")