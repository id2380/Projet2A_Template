from datetime import datetime


class Utilisateur:
    """
    Classe représentant un utilisateur dans l'application.

    Attributes
    ----------
    _id_utilisateur : int or None
        L'identifiant unique de l'utilisateur, généré automatiquement par la base de données.
    _pseudo : str
        Le pseudo de l'utilisateur, unique et non nul.
    _adresse_email : str
        L'adresse e-mail de l'utilisateur, unique et non nulle.
    _mot_de_passe : str
        Le mot de passe de l'utilisateur, stocké sous forme hashée.
    _date_creation : datetime or None
        La date de création du compte utilisateur, générée automatiquement par la base de données.
    """

    def __init__(self, pseudo: str, adresse_email: str, mot_de_passe: str):
        """
        Initialise un nouvel utilisateur avec les informations fournies.

        Parameters
        ----------
        pseudo : str
            Le pseudo de l'utilisateur.
        adresse_email : str
            L'adresse e-mail de l'utilisateur.
        mot_de_passe : str
            Le mot de passe de l'utilisateur (sera hashé ailleurs).
        """
        self._id_utilisateur = None  # L'ID utilisateur sera généré par la base de données
        self._pseudo = pseudo
        self._adresse_email = adresse_email
        self._mot_de_passe = mot_de_passe  # Le mot de passe sera hashé dans la classe utilisateur_service
        self._date_creation = None  # La date de création sera générée par la base de données

    @property
    def id_utilisateur(self) -> int:
        return self._id_utilisateur

    @id_utilisateur.setter
    def id_utilisateur(self, value: int):
        self._id_utilisateur = value

    @property
    def pseudo(self) -> str:
        return self._pseudo

    @pseudo.setter
    def pseudo(self, value: str):
        self._pseudo = value

    @property
    def adresse_email(self) -> str:
        return self._adresse_email

    @adresse_email.setter
    def adresse_email(self, value: str):
        self._adresse_email = value

    @property
    def mot_de_passe(self) -> str:
        return self._mot_de_passe

    @mot_de_passe.setter
    def mot_de_passe(self, value: str):
        self._mot_de_passe = value

    @property
    def date_creation(self) -> datetime:
        return self._date_creation

    @date_creation.setter
    def date_creation(self, value: datetime):
        self._date_creation = value
