CREATE DATABASE IF NOT EXISTS mydiscord;

USE mydiscord;

-- Table pour les utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    email VARCHAR(100),
    mot_de_passe VARCHAR(100)
);

-- Table pour les salons (channels)
CREATE TABLE IF NOT EXISTS channels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_du_salon VARCHAR(100)
);

-- Table pour les messages
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT,
    salon_id INT,
    message TEXT,
    FOREIGN KEY (utilisateur_id) REFERENCES users(id),
    FOREIGN KEY (salon_id) REFERENCES channels(id)
);
