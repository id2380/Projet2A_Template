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
    ):
        if title is None:
            films = FilmClient().recherche_films(page,
                                                 language,
                                                 primary_release_year)
        else:
            films = FilmClient().recherche_films_titre(title,
                                                       page,
                                                       language,
                                                       primary_release_year)
        if len(films) == 0:
            raise ValueError("Aucun film ne correspond à vos critères.")
        if primary_release_year is not None and films[1].date_de_sortie.year !=primary_release_year:
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
    valueError : Aucun film n'est similaire au film en paramètre.
    """
    def recherche_films_similaires(self,
                                   id_film: int,
                                   language: str = "fr",
                                   page: int = 1):
        films = FilmClient().obtenir_films_similaires(id_film, language, page)
        if len(films) == 0:
            raise ValueError("Aucun film n'est similaire au film.")
        return films

    """
    Permet de rechercher un film à partir de son identifiant.

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
        film = FilmClient().recherche_film_id(id_film)
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
    valueError : L'identifiant du film est non valide.
    valueError : Le film existe déjà dans la base.
    """
    def creer_film(self, id_film: int):
        film_dao = FilmDAO()
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
        film_dao.supprimer_film(id_film)

    """
    Renvoie des films présents dans la base. Le nombre est contrôlé par un
    paramètre "limite".

    Parameters
    ----------
    limite : int
        Le nombre de films maximum retournés.

    Retour
    ----------
    films : list[Film]
        La liste des films.

    Exception
    -------
    ValueError : erreur lors de la lecture des films dans la base.
    """
    def liste_films(self, limite: int = 100):
        return FilmDAO().liste_films(limite)

    """
    Teste si un film est présent dans la base de données.

    Parameters
    ----------
    id_film : int
        L'identifiant du film.

    Retour
    ----------
    bool : True si le film est présent, False sinon.

    Exception
    -------
    ValueError : erreur lors du test dans la base.

    """
    def existe_film(self, id_film: int):
        return FilmDAO().existe_film(id_film)

    """
    Renvoie un film existant dans la base de données.

    Parameters
    ----------
    id_film : int
        L'identifiant du film.

    Retour
    ----------
    Film : le film recherché.

    Exception
    -------
    ValueError : erreur lors de la recherche dans la base.

    """
    def lire_film(self, id_film: int):
        return FilmDAO().lire_film(id_film)