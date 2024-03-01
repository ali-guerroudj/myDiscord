import pygame
import sys

# Initialiser le jeu pygame
pygame.init()

# Définir les dimensions de la fenêtre
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 720

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Créer la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Charger l’image de fond
bg_image = pygame.image.load('image/bc1.png')

# Mettre à l’échelle l’image d’arrière-plan pour l’adapter à la taille de la fenêtre
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Définir le libellé de la fenêtre
pygame.display.set_caption("Menu")

# Charger l’image du logo
logo_image = pygame.image.load('image/zik2.png')
logo_width, logo_height = logo_image.get_size()  # Obtenir les dimensions originales du logo
logo_scale = 0.7  # Échelle du logo (50% de la taille d'origine)
logo_image = pygame.transform.smoothscale(logo_image, (int(logo_width * logo_scale), int(logo_height * logo_scale)))  # Redimensionner le logo

# Charger la nouvelle image
new_image = pygame.image.load('image/jeux.png')
new_width, new_height = new_image.get_size()  # Obtenir les dimensions originales de la nouvelle image
new_scale = 0.2  # Échelle de la nouvelle image (60% de la taille d'origine)
new_image = pygame.transform.smoothscale(new_image, (int(new_width * new_scale), int(new_height * new_scale)))  # Redimensionner la nouvelle image

# Charger l’image de la voiture
voiture_image = pygame.image.load('image/voiture.png')
voiture_width, voiture_height = voiture_image.get_size()  # Obtenir les dimensions originales de l'image de la voiture
voiture_scale = 0.5  # Échelle de l'image de la voiture (50% de la taille d'origine)
voiture_image = pygame.transform.smoothscale(voiture_image, (int(voiture_width * voiture_scale), int(voiture_height * voiture_scale)))  # Redimensionner l'image de la voiture

# Définir la position du logo
logo_position = (SCREEN_WIDTH // 2 - logo_image.get_width() // 2, SCREEN_HEIGHT // 2 - logo_image.get_height() // 2)

# Définir la position de la nouvelle image
new_image_position = (SCREEN_WIDTH // 2 + logo_image.get_width() // 0.8, SCREEN_HEIGHT // 3.2)

# Définir la position de la voiture
voiture_position = (10, SCREEN_HEIGHT // 2 - voiture_image.get_height() // 2)

# Définir la police et la taille du texte
font = pygame.font.Font(None, 100)

# Créer le texte
text = font.render("CHOISISSEZ VOTRE SALON", True, WHITE)

# Obtenir les dimensions du texte
text_width, text_height = font.size("Mon texte")

# Définir la position du texte
text_position = (SCREEN_WIDTH // 4.70 - text_width // 2, 50)

# Lancer la boucle du jeu
running = True
while running:
    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dessiner l’image de fond mise à l’échelle à la position (0,0)
    screen.blit(bg_image, (0, 0))
    
    # Dessinez le logo sur l’écran
    screen.blit(logo_image, logo_position)

    # Dessiner la nouvelle image à l’écran
    screen.blit(new_image, new_image_position)

    # Dessiner la voiture sur l’écran
    screen.blit(voiture_image, voiture_position)

    # Dessiner le texte sur l’écran
    screen.blit(text, text_position)

    # Mettre à jour l’affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()






 





