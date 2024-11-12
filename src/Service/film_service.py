from src.client.film_client import FilmClient
from src.dao.film_dao import FilmDAO


class FilmService:
    """
    Classe contenant les méthodes de service pour les films.
    """

    # -------------------------------------------------------------------------
    # Méthodes
    # -------------------------------------------------------------------------

    """
    Permet de rechercher une liste de films dans l'API Tmdb. Utilise la bonne
    fonction de recherche dans la classe FilmClient en fonction des critères
    de recherche.

    Paramètres
    ----------
    titre : str
        La chaîne de caractères qui doit être contenue dans le titre.
    page : int
        Le nombre de pages de films à charger dans l'API.
    language : str
        La langue utilisée dans l'API, par défaut c'est le français.
    primary_release_year : int
        L'année de première sortie du film.
    region : str
        La région où le film doit être disponible.
    year : int
        L'année de production du film.

    Retour
    ----------
    list[Film] : liste de films populaires remplissant les caractéristiques
    en paramètres

    Exception
    ----------
    ValueError : en cas de problème de communication avec l'API.
    ValueError : si aucun film ne correspond aux critères de la recherche.
    """
    def recherche_films(
        self,
        title: str = None,
        page: int = 1,
        language: str = "fr",
        primary_release_year: int = None,
        region: str = None,
        year: int = None,
    ):
        if title is None:
            films = FilmClient().recherche_films(page,
                                                 language,
                                                 primary_release_year,
                                                 region,
                                                 year)
        else:
            films = FilmClient().recherche_films_titre(title,
                                                       page,
                                                       language,
                                                       primary_release_year,
                                                       region,
                                                       year)
        if len(films) == 0:
            raise ValueError("Aucun film ne correspond à vos critères.")
        return films

    """
    Permet de rechercher une liste de films dans l'API Tmdb qui sont similaires
    au film passé en paramètre. 

    Paramètres
    ----------
    id_film : int
        L'identifiant du film.
    page : int
        Le nombre de pages de films à charger dans l'API.
    language : str
        La langue utilisée dans l'API, par défaut c'est le français.

    Retour
    ----------
    list[Film] : liste de films similaires.

    Exception
    ----------
    valueError : erreur de communication avec l'API.
    valueError : identifiant du film non valide.
    """
    def recherche_films_similaires(self,
                                   id_film: int,
                                   language: str = "fr",
                                   page: int = 1):
        films = FilmClient().obtenir_films_similaires(id_film, language, page)
        return films

    """
    Permet de rechercher un film à partir de son identifiant. Si il existe déjà
    dans la base, les informations sont recherchées dans la base, sinon elles sont
    recherchées sur l'API Tmdb.

    Paramètres
    ----------
    id_film : int
        L'identifiant du film.

    Retour
    ----------
    Film_Complet : Le film recherché.

    Exception
    ----------
    valueError : erreur de communication avec l'API.
    valueError : identifiant du film non valide.
    """
    def recherche_film_id(self, id_film: int):
        film_dao = FilmDAO()
        if film_dao.existe_film(id_film):
            film = film_dao.lire_film(id_film)
        else:
            film = FilmClient().recherche_film_id(id_film)
            film_dao.creer_film(film)
        return film

    """
    Permet de créer un film dans la base de données. Si il existe déjà
    dans la base, une erreur est renvoyé, sinon il est crée.

    Paramètres
    ----------
    id_film : int
        L'identifiant du film.

    Exception
    ----------
    valueError : Erreur de communication avec l'API.
    valueError : L'identifiant du film  est non valide.
    valueError : Le film existe déjà dans la base.
    """
    def creer_film(self, id_film: int):
        film_dao = FilmDAO()
        if film_dao.existe_film(id_film):
            raise ValueError("Le film existe déjà.")
        else:
            film = FilmClient().recherche_film_id(id_film)
            film_dao.creer_film(film)

    """
    Permet de supprimer un film de la base de données. Si il existe
    dans la base, il est supprimé, sinon une erreur est renvoyée.

    Paramètres
    ----------
    id_film : int
        L'identifiant du film.

    Exception
    ----------
    valueError : Erreur de communication avec l'API.
    valueError : L'identifiant du film  est non valide.
    valueError : Le film n'existe pas dans la base.
    """
    def supprimer_film(self, id_film: int):
        film_dao = FilmDAO()
        if not film_dao.existe_film(id_film):
            raise ValueError("Le film n'existe pas.")
        else:
            film_dao.supprimer_film(id_film)
