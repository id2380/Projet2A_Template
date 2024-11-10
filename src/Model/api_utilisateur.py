from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class APIUtilisateur(BaseModel):
    """
    Classe représentant un utilisateur dans l'application, héritant de BaseModel pour validation des données.

    Attributes
    ----------
    id_utilisateur : Optional[int]
        L'identifiant unique de l'utilisateur, généré automatiquement par la base de données.
    pseudo : str
        Le pseudo de l'utilisateur, unique et non nul.
    """

    id_utilisateur: Optional[int] = None
    pseudo: str
