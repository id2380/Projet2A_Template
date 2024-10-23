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
    """

    id_film: int = None
    titre: str = None
    genre: str = None
    date_de_sortie: str = None
    langue_originale: str = None
    synopsis: str = None
