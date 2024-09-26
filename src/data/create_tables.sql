CREATE TABLE IF NOT EXISTS utilisateur (
    id SERIAL PRIMARY KEY,                -- Identifiant unique, généré automatiquement
    username VARCHAR(50) UNIQUE NOT NULL, -- Nom d'utilisateur unique
    email VARCHAR(100) UNIQUE NOT NULL,   -- Email unique
    password_hash TEXT NOT NULL,          -- Mot de passe hashé
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Date de création
);
