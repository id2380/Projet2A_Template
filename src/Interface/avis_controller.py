from typing import TYPE_CHECKING
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.Interface.init_app import avis_service

if TYPE_CHECKING:
    from src.Model.avis import Avis

# Création du routeur pour l'API Avis
avis_router = APIRouter(prefix="/avis", tags=["Avis"])

# Modèle de requête pour la création d'avis (non nécessaire ici car utilisation des paramètres GET)
class RequeteCreationAvis(BaseModel):
    id_film: int
    utilisateur: str
    commentaire: str
    note: int

@avis_router.get("/creer_avis", status_code=status.HTTP_201_CREATED)
def creer_avis(id_film: int, utilisateur: str, commentaire: str, note: int):
    import dotenv
    dotenv.load_dotenv(override=True)
    try:
        # Création de l'avis avec l'ID du film fourni par l'utilisateur
        avis = avis_service.ajouter_avis(
            id_avis=None,
            id_film=id_film,  # Utilisation de l'ID du film fourni en paramètre
            utilisateur=utilisateur,
            note=note,
            commentaire=commentaire
        )

        # Vérification si l'avis a été créé avec succès
        if avis:
            return {"message": "Votre avis a été créé avec succès."}
        else:
            raise ValueError("La création de l'avis a échoué.")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la création de l'avis : {str(e)}")
