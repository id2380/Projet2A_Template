import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from src.Model.Movie import Movie
from src.Service.MovieService import MovieService
from src.Service.utilisateur_service import UtilisateurService
from src.Service.avis_service import AvisService



# Modèle pour la requête de création d'un compte utilisateur
class RequeteCreationCompte(BaseModel):
    pseudo: str
    adresse_email: str
    mot_de_passe: str

class RequeteCreationAvis(BaseModel):
    film: str
    utilisateur: str
    commentaire: str
    note: int


def run_app(movie_service: MovieService, utilisateur_service: UtilisateurService, avis_service: AvisService):
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @app.get("/movies/{tmdb_id}", status_code=status.HTTP_200_OK)
    def get_movie_by_id(tmdb_id: int) -> Movie:
        try:
            my_movie: Movie = movie_service.get_by_id(tmdb_id)
            return my_movie
        except FileNotFoundError:
            raise HTTPException(
                status_code=404,
                detail="Movie with id [{}] not found".format(tmdb_id),
            ) from FileNotFoundError
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid request")

    # Ajout d'une nouvelle route pour la création d'utilisateur
    @app.post("/creer_compte", status_code=status.HTTP_201_CREATED)
    def creer_compte(requete: RequeteCreationCompte):
        try:
            utilisateur = utilisateur_service.creation_compte(
                pseudo=requete.pseudo,
                adresse_email=requete.adresse_email,
                mot_de_passe=requete.mot_de_passe
            )
            # Vérification si l'utilisateur a été créé avec succès
            if utilisateur:
                return {
                    "message": f"Bravo ! L'utilisateur {utilisateur.pseudo} a été créé avec succès. Bienvenue dans notre super application Cinégramme"
                }
            else:
                raise ValueError("La création de l'utilisateur a échoué.")
        except Exception as e:
            import traceback
            print("Stack Trace:")
            traceback.print_exc()  # Cela affichera l'exception complète avec le stack trace
            raise HTTPException(status_code=400, detail=f"Erreur : {str(e)}")
        
    
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
    uvicorn.run(app, port=8000, host="localhost")
