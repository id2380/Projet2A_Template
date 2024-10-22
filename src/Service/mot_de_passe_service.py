import hashlib
import secrets
from typing import Optional

from src.dao.utilisateur_dao import UtilisateurDAO
from src.Model.utilisateur import Utilisateur


def hacher_mot_de_passe(mot_de_passe: str, sel: Optional[str] = None) -> str:
    """Hache le mot de passe avec un sel optionnel."""
    if sel is None:
        sel = secrets.token_hex(16)  # Générer un sel aléatoire si non fourni
    mot_de_passe_bytes = mot_de_passe.encode('utf-8') + sel.encode('utf-8')
    hash_object = hashlib.sha256(mot_de_passe_bytes)
    return hash_object.hexdigest()


def creer_sel() -> str:
    """Crée un sel aléatoire pour sécuriser le mot de passe."""
    return secrets.token_hex(16)


def verifier_robustesse_mot_de_passe(mot_de_passe: str):
    """Vérifie que le mot de passe respecte les critères de sécurité."""
    if len(mot_de_passe) < 8:
        raise Exception("Le mot de passe doit contenir au moins 8 caractères")


def valider_nom_utilisateur_mot_de_passe(
        nom_utilisateur: str, mot_de_passe: str, utilisateur_DAO: UtilisateurDAO
    ) -> Utilisateur:
    """
    Valide les informations d'authentification fournies par l'utilisateur.
    
    Parameters
    ----------
    nom_utilisateur : str
        Le nom d'utilisateur fourni par l'utilisateur.
    mot_de_passe : str
        Le mot de passe fourni par l'utilisateur.
    utilisateur_DAO: UtilisateurDAO
        La classe permettant d'accéder à la base de données et de gérer les utilisateurs.

    Returns
    -------
    Utilisateur
        L'utilisateur correspondant si l'authentification réussit.
    
    Raises
    ------
    Exception
        Si l'utilisateur ou le mot de passe est incorrect.
    """
    utilisateur_avec_nom: Optional[Utilisateur] = utilisateur_DAO.chercher_utilisateur_par_pseudo(nom_utilisateur=nom_utilisateur)

    if utilisateur_avec_nom is None:
        raise Exception("Nom d'utilisateur incorrect")

    # Vérifier le hachage du mot de passe avec celui enregistré dans la base
    mot_de_passe_hache = hacher_mot_de_passe(mot_de_passe, utilisateur_avec_nom.sel)  # Utiliser le sel de l'utilisateur
    if mot_de_passe_hache != utilisateur_avec_nom.mot_de_passe:
        raise Exception("Mot de passe incorrect")

    return utilisateur_avec_nom

