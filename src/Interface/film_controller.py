from fastapi import APIRouter, Depends, HTTPException, status

from src.Interface.jwt_bearer import JWTBearer
from src.Interface.user_controller import \
    obtenir_utilisateur_depuis_credentials
from src.service.avis_service import AvisService
from src.service.film_service import FilmService

film_router = APIRouter(prefix="/films", tags=["Films"])


@film_router.get("/recherche_films", status_code=status.HTTP_200_OK)
def recherche_films(titre: str = None,
                    language: str = "fr",
                    annee_de_sortie: int = None,
                    page: int = 1):
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        if page <= 0 or page > 500:
            raise ValueError("Le nombre de pages doit être entre 1 et 500.")
        films = FilmService().recherche_films(
            title=titre,
            language=language,
            primary_release_year=annee_de_sortie,
            page=page)
        return films
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@film_router.get("/recherche_films_similaires", status_code=status.HTTP_200_OK)
def recherche_films_similaires(id_film: int,
                               language: str = "fr",
                               page: int = 1):
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        if page <= 0 or page > 500:
            raise ValueError("Le nombre de pages doit être entre 1 et 500.")
        films = FilmService().recherche_films_similaires(id_film=id_film,
                                                         language=language,
                                                         page=page)
        return films
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")


@film_router.get("/informations_techniques", status_code=status.HTTP_200_OK)
def obtenir_fiche_technique(id_film: int):
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        film = FilmService().recherche_film_id(id_film=id_film)
        avis_service = AvisService()
        try:
            note_moyenne = avis_service.calculer_note_moyenne(id_film)
            avis = avis_service.obtenir_avis(id_film)
        except Exception:
            note_moyenne = None
            avis = None
        film.note_moyenne = note_moyenne
        film.avis = avis
        return film
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")
