from src.data.init_db import initialize_database
from src.Interface.API import run_app
from src.Service.MovieService import MovieService
from src.Service.utilisateur_service import UtilisateurService

if __name__ == "__main__":
    # Appel à la fonction pour initialiser la base de données
    initialize_database()

    # Instanciation des services
    movie_service = MovieService(None)
    utilisateur_service = UtilisateurService(None)

    # Appel à la fonction run_app avec les deux services
    app = run_app(movie_service=movie_service, utilisateur_service=utilisateur_service)
