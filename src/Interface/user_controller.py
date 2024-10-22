from typing import TYPE_CHECKING, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Model.api_utilisateur import APIUtilisateur
from src.Model.utilisateur import Utilisateur
from src.Model.jwt_response import JWTResponse
from src.Interface.init_app import jwt_service, utilisateur_service, utilisateur_dao
from src.Interface.jwt_bearer import JWTBearer
from src.Service.mot_de_passe_service import valider_nom_utilisateur_mot_de_passe
from pydantic import BaseModel

if TYPE_CHECKING:
    from src.Model.utilisateur import Utilisateur

user_router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])

class APIReponseCreationCompte(BaseModel):
    utilisateur: APIUtilisateur
    message: str

@user_router.post("/creer_compte", status_code=status.HTTP_201_CREATED, response_model=APIReponseCreationCompte)
def creer_compte(requete: Utilisateur) -> APIReponseCreationCompte:
    """
    Crée un nouvel utilisateur et renvoie les informations (tronquées) de l'utilisateur 
    et un message de bienvenue.
    """
    # Vérifier si le pseudo existe déjà
    if utilisateur_dao.chercher_utilisateur_par_pseudo(requete.pseudo):
        raise HTTPException(status_code=409, detail="Le pseudo existe déjà")

    try:
        # Création de l'utilisateur via le service
        utilisateur = utilisateur_service.creation_compte(
            pseudo=requete.pseudo, 
            adresse_email=requete.adresse_email, 
            mot_de_passe=requete.mot_de_passe
        )
    except Exception as error:
        raise HTTPException(status_code=400, detail="Erreur lors de la création de l'utilisateur") from error

    return APIReponseCreationCompte(
        utilisateur=APIUtilisateur(id_utilisateur=utilisateur.id_utilisateur, pseudo=utilisateur.pseudo),
        message=f"Bienvenue {utilisateur.pseudo} dans notre super application Cinégram !"
    )


@user_router.post("/jwt", status_code=status.HTTP_201_CREATED)
def connexion(pseudo: str, mot_de_passe: str) -> JWTResponse:
    """
    Authentifie l'utilisateur avec son pseudo et son mot de passe et retourne un token JWT.
    """
    try:
        utilisateur = valider_nom_utilisateur_mot_de_passe(
            nom_utilisateur=pseudo, 
            mot_de_passe=mot_de_passe, 
            utilisateur_DAO=utilisateur_dao  
        )
    except Exception as error:
        print(f"Erreur lors de la connexion : {error}")  # Log l'erreur dans le terminal
        raise HTTPException(status_code=403, detail="Combinaison nom d'utilisateur et mot de passe invalide") from error

    return jwt_service.encoder_jwt(utilisateur.id_utilisateur)


@user_router.get("/moi", dependencies=[Depends(JWTBearer())])
def recuperer_profil_utilisateur(credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]) -> APIUtilisateur:
    """
    Récupère le profil de l'utilisateur authentifié via JWT.
    """
    return obtenir_utilisateur_depuis_credentials(credentials)


def obtenir_utilisateur_depuis_credentials(credentials: HTTPAuthorizationCredentials) -> APIUtilisateur:
    """
    Valide le JWT et récupère l'utilisateur associé à ce token.
    """
    token = credentials.credentials
    user_id = int(jwt_service.valider_jwt_utilisateur(token))
    utilisateur = utilisateur_dao.chercher_utilisateur_par_id(user_id)  
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    return APIUtilisateur(id_utilisateur=utilisateur.id_utilisateur, pseudo=utilisateur.pseudo)
