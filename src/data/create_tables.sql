-- Table 'Utilisateur' pour stocker les informations des utilisateurs
CREATE TABLE IF NOT EXISTS utilisateur (
    id_utilisateur SERIAL PRIMARY KEY,                -- Identifiant unique, généré automatiquement
    pseudo VARCHAR(50) UNIQUE NOT NULL,               -- Nom d'utilisateur unique
    adresse_email VARCHAR(100) NOT NULL,              -- Email
    mot_de_passe TEXT NOT NULL,                       -- Mot de passe hashé
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,-- Date de création
    sel TEXT NOT NULL                                 -- Sel pour le hachage du mot de passe
);


-- Table 'Abonnes' pour représenter les abonnements entre les utilisateurs
CREATE TABLE IF NOT EXISTS abonne (
    id_utilisateur INTEGER NOT NULL,      -- Identifiant de l'utilisateur qui s'abonne, doit exister dans 'Utilisateur'
    id_eclaireur INTEGER NOT NULL,        -- Identifiant de l'utilisateur suivi (l'éclaireur), doit exister dans 'Utilisateur'
    PRIMARY KEY (id_utilisateur, id_eclaireur), -- Clé primaire composée, chaque abonnement est unique par utilisateur et éclaireur
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur) ON DELETE CASCADE, -- Supprime l'abonnement si l'utilisateur est supprimé
    FOREIGN KEY (id_eclaireur) REFERENCES utilisateur(id_utilisateur) ON DELETE CASCADE -- Supprime l'abonnement si l'éclaireur est supprimé
);

-- Table 'Film' pour stocker les informations sur les films
CREATE TABLE IF NOT EXISTS film (
    id_film INTEGER PRIMARY KEY,       -- Identifiant unique du film, fourni par l'API
    titre VARCHAR(200) NOT NULL,       -- Titre du film, requis
    genres TEXT[] DEFAULT '{}',        -- Genres du film (ex: Action, Comédie)
    date_de_sortie DATE,               -- Date de sortie du film
    langue_originale VARCHAR(100),     -- Langue originale du film
    synopsis VARCHAR(500)              -- Résumé ou description du film
);

-- Table 'Avis' pour stocker les avis laissés par les utilisateurs sur les films
CREATE TABLE IF NOT EXISTS avis (
    id SERIAL PRIMARY KEY,
    id_film INTEGER NOT NULL REFERENCES film(id_film),
    utilisateur VARCHAR(255) NOT NULL REFERENCES utilisateur(pseudo),
    note INTEGER NOT NULL,
    commentaire TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
