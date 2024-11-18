from typing import TYPE_CHECKING, Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

from src.Interface.init_app import (jwt_service, utilisateur_dao,
                                    utilisateur_service)
from src.Interface.jwt_bearer import JWTBearer
from src.Model.api_utilisateur import APIUtilisateur
from src.Model.jwt_response import JWTResponse
from src.Model.utilisateur import Utilisateur
from src.service.mot_de_passe_service import (
    valider_pseudo_utilisateur_mot_de_passe, verifier_robustesse_mot_de_passe)

if TYPE_CHECKING:
    from src.Model.utilisateur import Utilisateur

user_router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])

class APIReponseUtilisateur(BaseModel):
    utilisateur: APIUtilisateur
    message: str

class CreationCompteRequete(BaseModel):
    pseudo: str
    adresse_email: str
    mot_de_passe: str

@user_router.post("/creer_compte", status_code=status.HTTP_201_CREATED, response_model=APIReponseUtilisateur)
def creer_compte(requete: CreationCompteRequete) -> APIReponseUtilisateur:
    """
    Crée un nouvel utilisateur et renvoie les informations (tronquées) de l'utilisateur
    et un message de bienvenue.
    """
    # Vérifier si le pseudo existe déjà
    if utilisateur_dao.chercher_utilisateur_par_pseudo(requete.pseudo):
        raise HTTPException(status_code=409, detail="Le pseudo existe déjà")

    # Vérification de la robustesse du mot de passe
    try:
        verifier_robustesse_mot_de_passe(requete.mot_de_passe)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

    try:
        # Création de l'utilisateur via le service
        utilisateur = utilisateur_service.creation_compte(
            pseudo=requete.pseudo, adresse_email=requete.adresse_email, mot_de_passe=requete.mot_de_passe
        )
    except Exception as error:
        raise HTTPException(status_code=400, detail="Erreur lors de la création de l'utilisateur") from error

    return APIReponseUtilisateur(
        utilisateur=APIUtilisateur(id_utilisateur=utilisateur.id_utilisateur, pseudo=utilisateur.pseudo),
        message=f"Bienvenue {utilisateur.pseudo} dans notre super application Cinégram !",
    )


class AuthRequete(BaseModel):
    pseudo: str
    mot_de_passe: str


@user_router.post("/authentification", status_code=status.HTTP_201_CREATED)
def authentification(requete: AuthRequete) -> JWTResponse:
    """
    Authentifie l'utilisateur avec son pseudo et son mot de passe et retourne un token JWT.
    """
    try:
        utilisateur = valider_pseudo_utilisateur_mot_de_passe(
            pseudo=requete.pseudo, mot_de_passe=requete.mot_de_passe, utilisateur_DAO=utilisateur_dao
        )
    except Exception as error:
        print(f"Erreur lors de la connexion : {error}")  # Log l'erreur dans le terminal
        raise HTTPException(status_code=403, detail="Combinaison nom d'utilisateur et mot de passe invalide") from error

    return jwt_service.encode_jwt(utilisateur.id_utilisateur)


def obtenir_utilisateur_depuis_credentials(credentials: HTTPAuthorizationCredentials) -> APIUtilisateur:
    """
    Valide le JWT et récupère l'utilisateur associé à ce token.
    """
    token = credentials.credentials
    user_id = int(jwt_service.validate_user_jwt(token))
    utilisateur = utilisateur_dao.chercher_utilisateur_par_id(user_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    return APIUtilisateur(id_utilisateur=utilisateur.id_utilisateur, pseudo=utilisateur.pseudo)


@user_router.get("/mon_profil", response_model=APIUtilisateur)
def recuperer_profil_utilisateur(credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())) -> APIUtilisateur:
    """
    Récupère le profil de l'utilisateur authentifié via JWT.
    """
    return obtenir_utilisateur_depuis_credentials(credentials)

class ModificationPseudoRequete(BaseModel):
    nouveau_pseudo: str


@user_router.put("/modifier_pseudo", response_model=APIReponseUtilisateur)
def modifier_pseudo(
    requete: ModificationPseudoRequete,
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
) -> APIReponseUtilisateur:
    """
    Modifie le pseudo de l'utilisateur authentifié.
    """
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    utilisateur_modifie = utilisateur_service.modifier_pseudo(utilisateur.id_utilisateur, requete.nouveau_pseudo)
    if not utilisateur_modifie:
        raise HTTPException(status_code=400, detail="La modification du pseudo a échoué")
    return APIReponseUtilisateur(
        utilisateur=APIUtilisateur(id_utilisateur=utilisateur_modifie.id_utilisateur, pseudo=utilisateur_modifie.pseudo),
        message=f"Le pseudo a bien été modifié pour l'utilisateur {utilisateur_modifie.pseudo}."
    )


class ModificationEmailRequete(BaseModel):
    nouvelle_adresse_email: str


@user_router.put("/modifier_email", response_model=APIReponseUtilisateur)
def modifier_email(
    requete: ModificationEmailRequete,
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
) -> APIReponseUtilisateur:
    """
    Modifie l'adresse e-mail de l'utilisateur authentifié.
    """
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)
    utilisateur_modifie = utilisateur_service.modifier_adresse_email(utilisateur.id_utilisateur, requete.nouvelle_adresse_email)
    if not utilisateur_modifie:
        raise HTTPException(status_code=400, detail="La modification de l'adresse e-mail a échoué")
    return APIReponseUtilisateur(
        utilisateur=APIUtilisateur(id_utilisateur=utilisateur_modifie.id_utilisateur, pseudo=utilisateur_modifie.pseudo),
        message=f"L'adresse e-mail a bien été modifiée pour l'utilisateur {utilisateur_modifie.pseudo}."
    )


class ModificationMotDePasseRequete(BaseModel):
    nouveau_mot_de_passe: str


@user_router.put("/modifier_mot_de_passe", response_model=APIReponseUtilisateur)
def modifier_mot_de_passe(
    requete: ModificationMotDePasseRequete,
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
) -> APIReponseUtilisateur:
    """
    Modifie le mot de passe de l'utilisateur authentifié.
    """
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)

    try:
        verifier_robustesse_mot_de_passe(requete.nouveau_mot_de_passe)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

    utilisateur_modifie = utilisateur_service.modifier_mot_de_passe(utilisateur.id_utilisateur, requete.nouveau_mot_de_passe)
    if not utilisateur_modifie:
        raise HTTPException(status_code=400, detail="La modification du mot de passe a échoué")
    return APIReponseUtilisateur(
        utilisateur=APIUtilisateur(id_utilisateur=utilisateur_modifie.id_utilisateur, pseudo=utilisateur_modifie.pseudo),
        message=f"Le mot de passe a bien été modifié pour l'utilisateur {utilisateur_modifie.pseudo}."
    )

class APIReponseMessage(BaseModel):
    message: str

@user_router.delete("/supprimer_compte", response_model=APIReponseMessage)
def supprimer_compte(
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())
) -> APIReponseMessage:
    """
    Supprime le compte de l'utilisateur authentifié et invalide son jeton.
    """
    token = credentials.credentials
    utilisateur = obtenir_utilisateur_depuis_credentials(credentials)

    # Supprime le compte de l'utilisateur
    compte_supprime = utilisateur_service.supprimer_compte(utilisateur.id_utilisateur)
    if not compte_supprime:
        raise HTTPException(status_code=400, detail="La suppression du compte a échoué")
    
    # Ajouter le jeton à la blacklist
    jwt_service.blacklist.add(token)
    
    return APIReponseMessage(message=f"Le compte de l'utilisateur {utilisateur.pseudo} a été supprimé avec succès.")

@user_router.get("/lister_tous_les_utilisateurs", response_model=List[APIUtilisateur])
def lister_tous_les_utilisateurs(
    page: int = Query(1, ge=1, description="Numéro de la page, la première par défaut")
) -> List[APIUtilisateur]:
    """
    Liste tous les utilisateurs de l'application, avec pagination.
    La taille de la page est fixée à 10 utilisateurs (au maximum).
    """
    TAILLE_PAGE = 10  # Taille fixe de la page

    try:
        # Récupérer tous les utilisateurs
        utilisateurs = utilisateur_dao.lister_tous_les_utilisateurs()
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la récupération des utilisateurs",
        ) from error

    # Calcul des indices pour la pagination
    debut = (page - 1) * TAILLE_PAGE
    fin = debut + TAILLE_PAGE

    # Extraire les utilisateurs pour la page demandée
    utilisateurs_pagines = utilisateurs[debut:fin]

    # Vérifier si la page est vide
    if not utilisateurs_pagines:
        raise HTTPException(status_code=404, detail="Aucun utilisateur trouvé pour cette page")

    return [
        APIUtilisateur(id_utilisateur=u.id_utilisateur, pseudo=u.pseudo) 
        for u in utilisateurs_pagines
    ]


@user_router.get("/recherche_par_pseudo", response_model=List[APIUtilisateur])
def recherche_par_pseudo(
    pseudo_partiel: str = Query(
        ...,  # Indique que le paramètre est obligatoire
        description=(
        "Partie d'un pseudo à rechercher. Par exemple, "
        "'th' renverra 'Thibaut', 'Thierry', 'Agathe', etc. s'ils sont dans la base."
        )
    )
) -> List[APIUtilisateur]:
    """
    Recherche des utilisateurs à partir d'un pseudo partiel. 
    """
    utilisateurs = utilisateur_dao.chercher_utilisateurs_par_pseudo_partiel(pseudo_partiel)

    if not utilisateurs:
        raise HTTPException(status_code=404, detail="Aucun utilisateur trouvé")

    # Convertir chaque utilisateur en APIUtilisateur pour la réponse
    return [
        APIUtilisateur(id_utilisateur=u.id_utilisateur, pseudo=u.pseudo)
        for u in utilisateurs
    ]


