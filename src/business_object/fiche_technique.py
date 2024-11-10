from datetime import datetime


class FicheTechnique:
    """
    Une classe qui représente les informations techniques d'un film.
    """

    # -------------------------------------------------------------------------
    # Constructeur
    # -------------------------------------------------------------------------

    """
    Attributs
    ----------
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
    avis : Liste[Avis]
        Les avis associés au film.
    """

    def __init__(self, budget, pays_origine, societe_prod, duree, revenue, note_moyenne, avis) -> None:
        # -----------------------------
        # Attributs
        # -----------------------------

        self._budget: int = budget
        self._pays_origine: str = pays_origine
        self._societe_prod: str = societe_prod
        self._duree: int = duree
        self._revenue: int = revenue
        self._note_moyenne: float = note_moyenne
        self.avis = avis

    # -------------------------------------------------------------------------
    # Methodes
    # -------------------------------------------------------------------------

    def __str__(self):
        """
        Retourne un string représentant un objet FicheTechnique.
        """
        return (
            f"Budget: {self.budget}\n"
            f"Pays d'origine: {self.pays_origine}\n"
            f"Société de production : {self.societe_prod}\n"
            f"Durée : {self.duree}\n"
            f"Revenue : {self.revenue}\n"
        )

    # -------------------------------------------------------------------------
    # Getters et Setters
    # -------------------------------------------------------------------------

    @property
    def budget(self):
        return self._budget

    @budget.setter
    def budget(self, value: int):
        self._budget = value

    @property
    def pays_origine(self):
        return self._pays_origine

    @pays_origine.setter
    def pays_origine(self, value: str):
        self._pays_origine = value

    @property
    def societe_prod(self):
        return self._societe_prod

    @societe_prod.setter
    def societe_prod(self, value: str):
        self._societe_prod = value

    @property
    def duree(self):
        return self._duree

    @duree.setter
    def duree(self, value: int):
        self._duree = value

    @property
    def revenue(self):
        return self._revenue

    @revenue.setter
    def revenue(self, value: int):
        self._revenue = value

    @property
    def note_moyenne(self):
        return self._note_moyenne

    @note_moyenne.setter
    def note_moyenne(self, value: float):
        self._note_moyenne = value
