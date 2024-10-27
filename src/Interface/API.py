from typing import Optional

import uvicorn
from fastapi import FastAPI

from src.Interface.avis_controller import avis_router
from src.Interface.eclaireurs_controller import eclaireurs_router
from src.Interface.film_controller import film_router
from src.Interface.user_controller import user_router


def run_app():
    app = FastAPI(title="Cinégram", description="Application de gestion de films")

    app.include_router(user_router)

    app.include_router(film_router)

    #app.include_router(avis_router)

    #app.include_router(eclaireurs_router)

    uvicorn.run(app, port=8000, host="localhost")
