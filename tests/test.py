from src.business_object.avis import Avis
from src.dao.avis_dao import AvisDAO
from src.service.avis_service import AvisService
# Simulons les données d'entrée
id_film = 1184918
utilisateur = 'Soukayna'
note = 8  # Assure-toi que c'est bien un entier
commentaire = ' film!'  # Ceci est une chaîne
commentaire2= 'nul'
id_avis= 12
avis_service = AvisService()
#avis = avis_service.ajouter_avis( id_film=1184918, utilisateur='Soukayna',  commentaire='Great movie!',note=5)

#success = avis_service.modifier_avis( id_film=1184918, utilisateur='Soukayna',  commentaire='Great !',note=7)
supprimer= avis_service.supprimer_avis(id_film=1184918, utilisateur='Soukayna')