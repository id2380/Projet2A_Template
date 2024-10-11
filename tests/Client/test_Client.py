import pytest
from pydantic_core import ValidationError

from src.Client.MovieClient import MovieClient

def test_get_movies():
    MC = MovieClient()
    res = MC.get_movies()
    assert res == 200

def test_get_movie_id():
    MC = MovieClient()
    res = MC.get_movie_id(id=533535)
    assert res == 200