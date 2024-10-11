import uvicorn
from fastapi import FastAPI, HTTPException, status

from src.Model.Movie import Movie
from src.Service.MovieService import MovieService


def run_app(movie_service: MovieService):
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    

    uvicorn.run(app, port=8000, host="localhost")
