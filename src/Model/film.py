from datetime import date
from typing import Optional

from pydantic import BaseModel

from src.business_object.fiche_technique import FicheTechnique


class Film(BaseModel):
    """
    Une classe qui représente un film.
    """

    # -------------------------------------------------------------------------
    # Constructeur
    # -------------------------------------------------------------------------

    """
    Attributs
    ----------
    id_film : int
        Un identifiant unique du film.
    titre : string
        Le titre du film.
    genre : string
        Le genre du film.
    date_de_sortie : datetime
        Le jour, le mois et l'année de sortie du film.
    langue_originale : str
        La langue originale du film.
    synopsis : str
        Le résumé du film.
    """

    id_film: int = None
    titre: str = None
    genre: Optional[str] = None
    date_de_sortie: Optional[date] = None
    langue_originale: Optional[str] = None
    synopsis: Optional[str] = None

    class Config:
        """Rendre le modèle mutable après la création de l'objet."""

        allow_mutation = True
