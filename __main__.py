from src.Interface.API import run_app
from src.Service.MovieService import MovieService

from src.data.init_db import initialize_database

if __name__ == "__main__":
    initialize_database()
    movie_service = MovieService(None)
    app = run_app(movie_service=movie_service)
