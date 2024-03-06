import pygame
import sys
from pygame.locals import *

# Initialisation de Pygame
pygame.init()

# Définir les couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (200, 200, 200)

# Définir la résolution de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Créer la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Choix du Pseudo")

# Police de texte
font = pygame.font.Font(None, 36)

# Variables de texte
pseudo = ""
is_typing = True

# Boucle principale du programme
while is_typing:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                pseudo = pseudo[:-1]
            elif event.key == K_RETURN:
                is_typing = False
            else:
                pseudo += event.unicode

    # Effacer l'écran
    screen.fill(BLANC)

    # Afficher le texte
    text_surface = font.render("Choisissez votre pseudo :", True, NOIR)
    screen.blit(text_surface, (50, 50))
    pygame.draw.rect(screen, GRIS, (50, 150, SCREEN_WIDTH - 100, 50))
    pseudo_surface = font.render(pseudo, True, NOIR)
    screen.blit(pseudo_surface, (60, 160))

    pygame.display.flip()

# Code pour la fenêtre de chat ici...

