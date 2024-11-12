from datetime import datetime

"""
    Permet de convertir une chaîne de caractères en date.

    Paramètres
    ----------
    date : str
        La chaîne de caractères à convertir en date.

    Retour
    ----------
    datetime : La chaîne de caractères convertit.
    """


def parse_str(date: str):
    if date != "":
        return datetime.strptime(date, "%Y-%m-%d")
    return None