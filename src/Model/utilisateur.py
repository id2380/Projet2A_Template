from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Utilisateur(BaseModel):
    """
    Classe représentant un utilisateur dans l'application,
    héritant de BaseModel pour validation des données.

    Attributes
    ----------
    id_utilisateur : Optional[int]
        L'identifiant unique de l'utilisateur, généré automatiquement
        par la base de données.
    pseudo : str
        Le pseudo de l'utilisateur, unique et non nul.
    adresse_email : str
        L'adresse e-mail de l'utilisateur, unique et non nulle.
    mot_de_passe : str
        Le mot de passe de l'utilisateur, stocké sous forme hashée.
    date_creation : Optional[datetime]
        La date de création du compte utilisateur, générée automatiquement
        par la base de données.
    sel : Optional[str]
        Le sel utilisé pour sécuriser le mot de passe.
    """

    id_utilisateur: Optional[int] = None
    pseudo: str
    adresse_email: str
    mot_de_passe: str
    date_creation: Optional[datetime] = None
    sel: Optional[str] = None

    class Config:
        """Rendre le modèle mutable après la création de l'objet."""
        allow_mutation = True
