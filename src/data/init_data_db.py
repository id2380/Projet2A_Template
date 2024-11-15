from src.dao.avis_dao import AvisDAO
from src.dao.utilisateur_dao import UtilisateurDAO
from src.service.avis_service import AvisService
from src.service.utilisateur_service import UtilisateurService


def init_data():
    utilisateur_dao = UtilisateurDAO()
    utilisateur_service = UtilisateurService(utilisateur_dao)
    avis_service = AvisService()
    avis_dao = AvisDAO()

    Thibaut = utilisateur_dao.chercher_utilisateur_par_pseudo("Thibaut")
    if not Thibaut:
        Thibaut = utilisateur_service.creation_compte(
            pseudo="Thibaut",
            adresse_email="thibaut@ensai.fr",
            mot_de_passe="Mdp Thibaut"
        )

    Soukayna = utilisateur_dao.chercher_utilisateur_par_pseudo("Soukayna")
    if not Soukayna:
        Soukayna = utilisateur_service.creation_compte(
            pseudo="Soukayna",
            adresse_email="soukayna@ensai.fr",
            mot_de_passe="Mdp Soukayna"
        )

    Jules = utilisateur_dao.chercher_utilisateur_par_pseudo("Jules")
    if not Jules:
        Jules = utilisateur_service.creation_compte(
            pseudo="Jules",
            adresse_email="jules@ensai.fr",
            mot_de_passe="Mdp Jules"
        )

    Gabrielle = utilisateur_dao.chercher_utilisateur_par_pseudo("Gabrielle")
    if not Gabrielle:
        Gabrielle = utilisateur_service.creation_compte(
            pseudo="Gabrielle",
            adresse_email="gabrielle@ensai.fr",
            mot_de_passe="Mdp Gabrielle"
        )

    Fanny = utilisateur_dao.chercher_utilisateur_par_pseudo("Fanny")
    if not Fanny:
        Fanny = utilisateur_service.creation_compte(
            pseudo="Fanny",
            adresse_email="fanny@ensai.fr",
            mot_de_passe="Mdp Fanny"
        )

    if len(avis_dao.lire_avis(id_film=1184918, id_utilisateur=Thibaut.id_utilisateur)) == 0 :
        avis_service.ajouter_avis(
            id_film=1184918,
            id_utilisateur=Thibaut.id_utilisateur,
            note=8,
            commentaire="Ce film est vraiment génial. J'ai adoré la qualité des dessins."
        )

    if len(avis_dao.lire_avis(id_film=1184918, id_utilisateur=Soukayna.id_utilisateur)) == 0 :
        avis_service.ajouter_avis(
            id_film=1184918,
            id_utilisateur=Soukayna.id_utilisateur,
            note=5,
            commentaire="Nul ! J'ai eu peur du robot."
        )

    if len(avis_dao.lire_avis(id_film=1184918, id_utilisateur=Jules.id_utilisateur)) == 0 :
        avis_service.ajouter_avis(
            id_film=1184918,
            id_utilisateur=Jules.id_utilisateur,
            note=10,
            commentaire="Masterclass"
        )

    if len(avis_dao.lire_avis(id_film=530, id_utilisateur=Fanny.id_utilisateur)) == 0 :
        avis_service.ajouter_avis(
            id_film=530,
            id_utilisateur=Fanny.id_utilisateur,
            note=5,
            commentaire="Bof"
        )

    if len(avis_dao.lire_avis(id_film=530, id_utilisateur=Gabrielle.id_utilisateur)) == 0 :
        avis_service.ajouter_avis(
            id_film=530,
            id_utilisateur=Gabrielle.id_utilisateur,
            note=1
        )

    if len(avis_dao.lire_avis(id_film=530, id_utilisateur=Thibaut.id_utilisateur)) == 0 :
        avis_service.ajouter_avis(
            id_film=530,
            id_utilisateur=Thibaut.id_utilisateur,
            note=4,
            commentaire="Très long. J'ai regardé ce film en 3 fois."
        )

    if len(avis_dao.lire_avis(id_film=140607, id_utilisateur=Soukayna.id_utilisateur)) == 0 :
        avis_service.ajouter_avis(
            id_film=140607,
            id_utilisateur=Soukayna.id_utilisateur,
            note=10,
            commentaire="Bizarrrrrre"
        )

    if len(avis_dao.lire_avis(id_film=140607, id_utilisateur=Gabrielle.id_utilisateur)) == 0 :
        avis_service.ajouter_avis(
            id_film=140607,
            id_utilisateur=Gabrielle.id_utilisateur,
            note=8,
            commentaire="Un peu niche"
        )

    if len(avis_dao.lire_avis(id_film=140607, id_utilisateur=Jules.id_utilisateur)) == 0 :
        avis_service.ajouter_avis(
            id_film=140607,
            id_utilisateur=Jules.id_utilisateur,
            note=6,
            commentaire="Sympa"
        )

    if len(avis_dao.lire_avis(id_film=199, id_utilisateur=Fanny.id_utilisateur)) == 0 :
        avis_service.ajouter_avis(
            id_film=199,
            id_utilisateur=Fanny.id_utilisateur,
            note=10
        )

    if len(avis_dao.lire_avis(id_film=175, id_utilisateur=Thibaut.id_utilisateur)) == 0 :
        avis_service.ajouter_avis(
            id_film=175,
            id_utilisateur=Thibaut.id_utilisateur,
            note=10,
            commentaire="Excellent"
        )

    if len(avis_dao.lire_avis(id_film=175, id_utilisateur=Soukayna.id_utilisateur)) == 0 :
        avis_service.ajouter_avis(
            id_film=175,
            id_utilisateur=Soukayna.id_utilisateur,
            note=9,
            commentaire="Top mais je n'ai pas vu le film."
        )

    if len(avis_dao.lire_avis(id_film=181808, id_utilisateur=Gabrielle.id_utilisateur)) == 0 :
        avis_service.ajouter_avis(
            id_film=181808,
            id_utilisateur=Gabrielle.id_utilisateur,
            note=6,
            commentaire="Mouais"
        )


if __name__ == "__main__":
    init_data()
