from dotenv import load_dotenv

from src.dao.utilisateur_dao import UtilisateurDAO
from src.Service.jwt_service import JwtService
from src.Service.utilisateur_service import UtilisateurService

load_dotenv()
utilisateur_dao = UtilisateurDAO()
jwt_service = JwtService()
utilisateur_service = UtilisateurService(utilisateur_dao)