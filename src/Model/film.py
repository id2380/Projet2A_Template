from datetime import datetime
from src.business_object.fiche_technique import FicheTechnique
from pydantic import BaseModel


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
    fiche_technique : FicheTechnique
        La fiche technique associée au film.
    """

    id_film: int
    titre: str
    genre: str
    date_de_sortie: datetime
    langue_originale: str
    synopsis: str
