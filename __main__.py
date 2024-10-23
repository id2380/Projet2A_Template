from src.data.init_db import initialize_database
from src.Interface.API import run_app

if __name__ == "__main__":
    # Appel à la fonction pour initialiser la base de données
    initialize_database()

    # Lancer l'application FastAPI
    app = run_app()
