from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Interface.jwt_bearer import JWTBearer
from src.Interface.user_controller import \
    obtenir_utilisateur_depuis_credentials
from src.service.avis_service import AvisService
from src.service.film_service import FilmService

film_router = APIRouter(prefix="/films", tags=["Films"])


@film_router.get("/recherche_films", status_code=status.HTTP_200_OK)
def recherche_films(titre: str = Query(None, description="Titre partiel du film."),
                    language: str = Query("fr", description="Langue utilisée pour le retour."),
                    annee_de_sortie: int = Query(None, description="L'année de sortie du film."),
                    page: int = Query(1, description="Le numéro de la page.")):
    """Permet d'obtenir une liste de films selon les critères utilisés. Par
    défaut, ce sont les 20 films les plus populaires (selon l'API TMDB)
    correspondant aux critères. En choisissant un numéro de page plus élevé,
    d'autres films sont proposés."""
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
def recherche_films_similaires(id_film: int = Query(..., description="L'identifiant du film."),
                               language: str = Query("fr", description="Langue utilisée pour le retour."),
                               page: int = Query(1, description="Le numéro de la page.")):
    """Permet d'obtenir une liste de films populaires (selon l'API TMDB)
    proches du film passé en ID. En choisissant un numéro de page plus élevé,
    d'autres films sont proposés."""
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


@film_router.get("/fiche_technique", status_code=status.HTTP_200_OK)
def obtenir_fiche_technique(id_film: int = Query(..., description="L'identifiant du film.")):
    "Permet d'obtenir la fiche technique du film passé en paramètre."
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


@film_router.get("/watchedlist", status_code=status.HTTP_200_OK)
def watchedlist(
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
):
    """
    Renvoie la watchedlist, la liste des films déjà vu (que l'utilisateur a
    noté) , de l'utilisateur.
    """
    import dotenv
    dotenv.load_dotenv(override=True)
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    avis_service = AvisService()
    try:
        return avis_service.watched_list(
                id_utilisateur=utilisateur.id_utilisateur
                )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erreur : {str(e)}")
