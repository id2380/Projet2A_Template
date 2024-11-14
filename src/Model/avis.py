from datetime import date
from typing import Optional

from pydantic import BaseModel


class Avis(BaseModel):
    """
    Une classe qui représente un avis.
    """

    # -------------------------------------------------------------------------
    # Constructeur
    # -------------------------------------------------------------------------

    """
    Attributs
    ----------
    id_film : int
        Un identifiant unique d'un film.
    id_utilisateur : int
        Un identifiant unique d'un utilisateur.
    note : int
        La note du film par l'utilisateur.
    commentaire : str
        Le commentaire du film par l'utilisateur.
    """

    id_film: int = None
    id_utilisateur: int = None
    note: int = None
    commentaire: Optional[str] = None

    class Config:
        """Rendre le modèle mutable après la création de l'objet."""

        allow_mutation = True
