CREATE DATABASE IF NOT EXISTS mydiscord;

USE mydiscord;

-- Table pour les utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100)
);

-- Table pour les salons (channels)
CREATE TABLE IF NOT EXISTS channels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

-- Table pour les messages
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(100),
    content text,
    timestamp datetime not null default current_timestamp,
    channel_id int,
    FOREIGN KEY (channels_id) REFERENCES channels(id)
);