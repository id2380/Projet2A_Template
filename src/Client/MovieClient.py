import json
import requests

from src.utils.singleton import Singleton

class MovieClient(metaclass=Singleton):
    def __init__(self) -> None:
        # Using an environment variable defined in the .env file
        self.__HOST = "https://api.themoviedb.org/3/"
        self._headers = {"accept": "application/json","Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0OTJhMmU0OTUyOTcwZDBmNWQ4ZTZiMjI2ZmFmZGMwNCIsIm5iZiI6MTcyNjgyMDY4My4zMDYxMjYsInN1YiI6IjY2ZWQyYzNiY2RkMTA4ZWQ5MzIyYWYzNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.2vVcbaxM_PX11RFgys6jhTskiwiV1t0fCChn8K0Hlxs"}
    
    def get_movies(self):
        url = f"{self.__HOST}discover/movie?include_adult=false"
        req = requests.get(url, headers=self._headers)
        return req.status_code

    def get_movie_id(self,id:int):
         url = f"{self.__HOST}movie/{id}"
         print(f"url :   {url}")
         req = requests.get(url, headers=self._headers)

         return req.status_code

