from datetime import datetime
from src.business_object.fiche_technique import FicheTechnique
from pydantic import BaseModel


class FilmComplet(BaseModel):

    """
    Une classe qui représente un film complet.
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
    budget : int
        Le budget du film.
    pays_origine : str
        Le pays d'origine du film.
    societe_prod : str
        La société de production du film.
    duree : int
        La durée du film.
    revenue : int
        Le revenue du film.
    note_moyenne : float
        La note moyenne du film.
    avis : list
        Les avis associés au film.
    """

    id_film: int
    titre: str
    genre: str
    date_de_sortie: datetime
    langue_originale: str
    synopsis: str
    budget: int
    pays_origine: str
    societe_prod: str
    duree: int
    revenue: int
    note_moyenne: float = None
    avis: list = None
