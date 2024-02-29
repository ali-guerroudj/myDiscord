import pygame
import mysql.connector
from mysql.connector import connect, Error

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLEU = (0, 0, 255)
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
violetred4 = (139, 34, 82, 255)

# Définition de la résolution de la fenêtre
res = (940, 800)

# Création de la fenêtre
window_surface = pygame.display.set_mode(res)
pygame.display.set_caption("Fenêtre d'inscription")

# Police de texte avec une taille spécifique
font = pygame.font.SysFont(None, 36)

# Charger l'image d'arrière-plan
bg_image = pygame.image.load('image/bc1.png')

# Redimensionner l'image pour qu'elle corresponde à la résolution de la fenêtre
bg_image = pygame.transform.scale(bg_image, res)

# Position et dimension du carré de connexion
carré_x = 200
carré_y = 200
carré_largeur = 500
carré_hauteur = 500

# Variables pour stocker le contenu des champs de saisie
email_text = ""
mdp_text = ""

# Variable pour suivre le champ actif
active_field = None

# Définir le temps de clignotement du curseur en millisecondes
BLINK_TIME = 500  # 500 ms

# Définir le temps du dernier clignotement
last_blink = pygame.time.get_ticks()

# Indicateur pour savoir si le curseur est visible
cursor_visible = False

# Définition des propriétés du bouton
bouton_x = 300
bouton_y = 450
bouton_largeur = 200
bouton_hauteur = 50
couleur_bouton_normal = (50, 205, 50)  # Vert
couleur_bouton_survol = (0, 255, 0)     # Vert clair

# Fonction pour établir la connexion à la base de données
def connecter_bdd():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="conan",
            database="mydiscord",
            auth_plugin='mysql_native_password'
        )
        return conn
    except Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None


# Fonction pour insérer un nouvel utilisateur dans la base de données
def inserer_utilisateur(conn, email, mot_de_passe):
    try:
        cursor = conn.cursor()
        insert_query = "INSERT INTO users (email, mot_de_passe) VALUES (%s, %s)"
        values = (email, mot_de_passe)
        cursor.execute(insert_query, values)
        conn.commit()
        print("Utilisateur inséré avec succès !")
    except Error as e:
        print(f"Erreur lors de l'insertion de l'utilisateur dans la base de données: {e}")

# Boucle principale du jeu
launched = True
while launched:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False
        elif event.type == pygame.KEYDOWN:
            if active_field == 'email':
                if event.key == pygame.K_BACKSPACE:
                    email_text = email_text[:-1]  # Supprimer le dernier caractère
                elif len(email_text) < 100:
                    email_text += event.unicode
            elif active_field == 'password':
                if event.key == pygame.K_BACKSPACE:
                    mdp_text = mdp_text[:-1]  # Supprimer le dernier caractère
                elif len(mdp_text) < 100:
                    mdp_text += event.unicode

        # Gérer le focus sur les champs de saisie
        elif event.type == pygame.MOUSEBUTTONDOWN:
            email_rect = pygame.Rect(carré_x + 100, carré_y + 100, 200, 30)
            password_rect = pygame.Rect(carré_x + 100, carré_y + 170, 200, 30)
            if email_rect.collidepoint(event.pos):
                active_field = 'email'
            elif password_rect.collidepoint(event.pos):
                active_field = 'password'
            else:
                active_field = None
                
            # Vérifier si la souris est cliquée sur le bouton de connexion
            if bouton_x < event.pos[0] < bouton_x + bouton_largeur and bouton_y < event.pos[1] < bouton_y + bouton_hauteur:
                print("Bouton de connexion cliqué !")  # Ici, vous pouvez ajouter votre logique de connexion
                
                # Établir une connexion à la base de données
                conn = connecter_bdd()
                if conn:
                    # Insérer l'utilisateur dans la base de données
                    inserer_utilisateur(conn, email_text, mdp_text)
                    # Fermer la connexion
                    conn.close()

    # Effacer l'écran
    window_surface.fill(BLANC)

    # Dessiner l'image d'arrière-plan redimensionnée
    window_surface.blit(bg_image, (0, 0))

    # Afficher le carré de connexion
    pygame.draw.rect(window_surface, violetred4, (carré_x, carré_y, carré_largeur, carré_hauteur))
    text_connexion = font.render("inscription", True, BLANC)
    window_surface.blit(text_connexion, (carré_x + 50, carré_y + 40))

    # Afficher les champs de saisie avec le texte saisi
    pygame.draw.rect(window_surface, NOIR, (carré_x + 100, carré_y + 100, 200, 30), 2)  # Champ E-mail
    pygame.draw.rect(window_surface, NOIR, (carré_x + 100, carré_y + 170, 200, 30), 2)  # Champ Mot de passe

    # Afficher le texte saisi dans le champ actif
    email_surface = font.render(email_text, True, NOIR)
    window_surface.blit(email_surface, (carré_x + 105, carré_y + 105))

    mdp_surface = font.render("*" * len(mdp_text), True, NOIR)  # Pour masquer le mot de passe
    window_surface.blit(mdp_surface, (carré_x + 105, carré_y + 175))

    # Afficher les labels des champs
    email_label = font.render("E-mail:", True, NOIR)
    window_surface.blit(email_label, (carré_x + 50, carré_y + 70))
    mdp_label = font.render("Mot de passe:", True, NOIR)
    window_surface.blit(mdp_label, (carré_x + 50, carré_y + 145))

    # Dessiner le bouton de connexion
    pygame.draw.rect(window_surface, couleur_bouton_normal, (bouton_x, bouton_y, bouton_largeur, bouton_hauteur))
    text_bouton = font.render("Connexion", True, BLANC)
    window_surface.blit(text_bouton, (bouton_x + 50, bouton_y + 15))

    # Actualiser l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
