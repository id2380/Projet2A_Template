from typing import Optional

import uvicorn
from fastapi import FastAPI

from src.Interface.user_controller import user_router
from src.Interface.film_controller import film_router


def run_app():
    app = FastAPI(title="Cinégram", description="Application de gestion de films")

    app.include_router(user_router)

    app.include_router(film_router)

    uvicorn.run(app, port=8000, host="localhost")
