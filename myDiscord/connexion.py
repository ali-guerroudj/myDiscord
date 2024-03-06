import pygame
import mysql.connector
import subprocess

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
pygame.display.set_caption("Fenêtre de Connexion")

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
password_text = ""

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

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sirinepupuce1",
    database="mydiscord"
)
cursor = conn.cursor()

# Fonction pour vérifier les informations de connexion
def verifier_connexion(email, mdp):
    # Exécutez la requête pour vérifier les informations de connexion dans la base de données
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password_text))
    result = cursor.fetchone()
    return result is not None

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
                elif len(email_text) < 20:
                    email_text += event.unicode
            elif active_field == 'password':
                if event.key == pygame.K_BACKSPACE:
                    password_text = password_text[:-1]  # Supprimer le dernier caractère
                elif len(password_text) < 20:
                    password_text += event.unicode

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
                if verifier_connexion(email_text, password_text):
                    print("Connexion réussie ! Redirection vers la page chat_general.py...")
                    subprocess.Popen(["python", "chat_general.py"])  # Lancer chat_general.py dans un nouveau processus
                    launched = False  # Terminer la boucle principale
                else:
                    print("Échec de la connexion. Veuillez vérifier vos informations.")

    # Effacer l'écran
    window_surface.fill(BLANC)

    # Dessiner l'image d'arrière-plan redimensionnée
    window_surface.blit(bg_image, (0, 0))

    # Afficher le carré de connexion
    pygame.draw.rect(window_surface, violetred4, (carré_x, carré_y, carré_largeur, carré_hauteur))
    text_connexion = font.render("CONNEXION", True, BLANC)
    window_surface.blit(text_connexion, (carré_x + 50, carré_y + 40))

    # Afficher les champs de saisie avec le texte saisi
    pygame.draw.rect(window_surface, NOIR, (carré_x + 100, carré_y + 100, 200, 30), 2)  # Champ E-mail
    pygame.draw.rect(window_surface, NOIR, (carré_x + 100, carré_y + 170, 200, 30), 2)  # Champ Mot de passe

    # Afficher le texte saisi dans le champ actif
    email_surface = font.render(email_text, True, NOIR)
    window_surface.blit(email_surface, (carré_x + 105, carré_y + 105))

    password_surface = font.render("*" * len(password_text), True, NOIR)  # Pour masquer le mot de passe
    window_surface.blit(password_surface, (carré_x + 105, carré_y + 175))

    # Afficher les labels des champs
    email_label = font.render("E-mail:", True, NOIR)
    window_surface.blit(email_label, (carré_x + 50, carré_y + 70))
    password_label = font.render("Mot de passe:", True, NOIR)
    window_surface.blit(password_label, (carré_x + 50, carré_y + 145))

    # Dessiner le bouton de connexion
    pygame.draw.rect(window_surface, couleur_bouton_normal, (bouton_x, bouton_y, bouton_largeur, bouton_hauteur))
    text_bouton = font.render("Connexion", True, BLANC)
    window_surface.blit(text_bouton, (bouton_x + 50, bouton_y + 15))

    # Faire clignoter le curseur
    if pygame.time.get_ticks() - last_blink >= BLINK_TIME:  # Chaque 500 millisecondes
        cursor_visible = not cursor_visible
        last_blink = pygame.time.get_ticks()

    if cursor_visible and active_field:
        cursor_rect = pygame.Rect(carré_x + 105 + font.size(email_text if active_field == 'email' else password_text)[0],
                                 carré_y + 105 if active_field == 'email' else carré_y + 175, 2,
                                 font.size(email_text if active_field == 'email' else password_text)[1])
        pygame.draw.rect(window_surface, NOIR, cursor_rect)

    # Actualiser l'affichage
    pygame.display.flip()

# Fermer la connexion à la base de données
conn.close()

# Quitter Pygame
pygame.quit()

