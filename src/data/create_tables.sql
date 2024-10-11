-- Table 'Utilisateur' pour stocker les informations des utilisateurs
CREATE TABLE IF NOT EXISTS Utilisateur (
    id_utilisateur SERIAL PRIMARY KEY,                -- Identifiant unique, généré automatiquement
    pseudo VARCHAR(50) UNIQUE NOT NULL, -- Nom d'utilisateur unique
    adresse_email VARCHAR(100) UNIQUE NOT NULL,   -- Email unique
    mot_de_passe TEXT NOT NULL,          -- Mot de passe hashé
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Date de création
);

-- Table 'Abonnes' pour représenter les abonnements entre les utilisateurs
CREATE TABLE IF NOT EXISTS Abonne (
    id_utilisateur INTEGER NOT NULL,      -- Identifiant de l'utilisateur qui s'abonne, doit exister dans 'Utilisateur'
    id_eclaireur INTEGER NOT NULL,        -- Identifiant de l'utilisateur suivi (l'éclaireur), doit exister dans 'Utilisateur'
    PRIMARY KEY (id_utilisateur, id_eclaireur), -- Clé primaire composée, chaque abonnement est unique par utilisateur et éclaireur
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateur(id_utilisateur) ON DELETE CASCADE, -- Supprime l'abonnement si l'utilisateur est supprimé
    FOREIGN KEY (id_eclaireur) REFERENCES Utilisateur(id_utilisateur) ON DELETE CASCADE -- Supprime l'abonnement si l'éclaireur est supprimé
);

-- Table 'Film' pour stocker les informations sur les films
CREATE TABLE IF NOT EXISTS Film (
    id_film PRIMARY KEY,               -- Identifiant unique du film, fourni par l'API
    titre VARCHAR(200) NOT NULL,       -- Titre du film, requis
    genre VARCHAR(100),                -- Genre du film (ex: Action, Comédie)
    date_de_sortie DATE,               -- Date de sortie du film
    langue_originale VARCHAR(100),     -- Langue originale du film
    synopsis VARCHAR(500)              -- Résumé ou description du film
);

-- Table 'Avis' pour stocker les avis laissés par les utilisateurs sur les films
CREATE TABLE IF NOT EXISTS Avis (
    id_utilisateur INTEGER NOT NULL,          -- Identifiant de l'utilisateur qui a laissé l'avis, doit exister dans 'Utilisateur'
    id_film INTEGER NOT NULL,                 -- Identifiant du film auquel l'avis se réfère, doit exister dans 'Film'
    note INTEGER CHECK (note BETWEEN 0 AND 10), -- Note attribuée au film, contrainte pour que la note soit entre 0 et 10
    commentaire VARCHAR(400),                 -- Commentaire de l'utilisateur sur le film (facultatif)
    PRIMARY KEY (id_utilisateur, id_film),    -- Clé primaire composée, chaque avis est unique par utilisateur et film
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateur(id_utilisateur) ON DELETE CASCADE, -- Supprime l'avis si l'utilisateur est supprimé
    FOREIGN KEY (id_film) REFERENCES Film(id_film) ON DELETE CASCADE -- Supprime l'avis si le film est supprimé
);

