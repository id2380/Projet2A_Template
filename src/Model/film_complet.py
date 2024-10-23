from datetime import datetime
from src.business_object.fiche_technique import FicheTechnique
from src.Model.film import Film


class FilmComplet(Film):

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

    budget: int = None
    pays_origine: str = None
    societe_prod: str = None
    duree: int = None
    revenue: int = None
    note_moyenne: float = None
    avis: list = None
