import pygame
import pygame_textinput
import sys

# Initialisation de Pygame
pygame.init()

# Récupération des dimensions de l'écran
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Définition d'une taille réduite pour la fenêtre
window_width = int(screen_width * 0.9)
window_height = int(screen_height * 0.9)

# Définition des couleurs
black = (0, 0, 0)
white = (255, 255, 255)

# Création de la fenêtre
screen = pygame.display.set_mode((window_width, window_height))

# Chargement de l'image de fond
background_image = pygame.image.load("image/bc1.png").convert()
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Chargement de l'image "send1.png" et redimensionnement
send_image = pygame.image.load("image/send1.png").convert_alpha() # Utilisation de convert_alpha() pour la transparence
send_image = pygame.transform.scale(send_image, (50, 50)) # Redimensionner l'image à la taille désirée

# Définition de la police
font = pygame.font.SysFont(None, 30)

# Liste des onglets
tabs = ["Automobile", "Cinéma", "Sport"]

# Calcul des dimensions de la barre de navigation
tab_width = window_width // len(tabs) // 3 # Largeur ajustée pour les onglets (réduite davantage)
tab_height = window_height // len(tabs)

# Définition de l'espacement vertical entre les textes (réduit)
text_vertical_spacing = 10

# Position et taille des rectangles blancs
rectangle1_width = 1050
rectangle1_height = 500
rectangle1_x = 250
rectangle1_y = 50

rectangle2_width = 1050
rectangle2_height = 150
rectangle2_x = window_width - rectangle2_width - 80
rectangle2_y = window_height - rectangle2_height - 50

# Rayon des coins arrondis pour les rectangles blancs
corner_radius = 20

# Création de l'objet TextInputVisualizer
textinput = pygame_textinput.TextInputVisualizer()

# Initialisation du texte et de la position du curseur
text_bottom = ""
text_top = ""
cursor_x = rectangle2_x + 10
cursor_y = rectangle2_y + 10

# Position de l'image "send1.png"
send_image_rect = send_image.get_rect()
send_image_rect.topleft = (window_width - 120, window_height - 100) # Ajustez ces valeurs pour positionner l'image

# Boucle principale
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Vérifier si le clic est effectué sur l'image "send1.png"
            if send_image_rect.collidepoint(event.pos):
                # Copier le texte du rectangle du bas vers le rectangle du haut
                text_top = text_bottom

        else:
            textinput.update(events)
            if event.type == pygame.KEYDOWN:
                # Vérifier si le nombre de lignes actuelles est inférieur à quatre
                if text_bottom.count('\n') < 4:
                    if event.key == pygame.K_BACKSPACE:
                        if text_bottom:
                            text_bottom = text_bottom[:-1]
                    elif event.key == pygame.K_RETURN:
                        text_bottom += "\n"
                    else:
                        # Limiter les caractères par ligne à 78
                        if len(text_bottom) % 78 == 0:
                            text_bottom += "\n"
                        text_bottom += event.unicode
                # Vérifier si la quatrième ligne contient déjà 78 caractères
                elif text_bottom.count('\n') == 3 and len(text_bottom.split('\n')[3]) < 78:
                    text_bottom += event.unicode

    # Calculer la hauteur totale du texte
    text_surface_bottom = font.render(text_bottom, True, black)
    text_surface_top = font.render(text_top, True, black)
    text_height_bottom = text_surface_bottom.get_height()
    text_height_top = text_surface_top.get_height()

    # Vérifier si la hauteur du texte dépasse la hauteur du rectangle
    if text_height_bottom > rectangle2_height:
        # Gérer le débordement : tronquer le texte ou implémenter un défilement
        # Pour simplifier, cette exemple tronque simplement le texte
        lines = text_bottom.split('\n')
        truncated_text = '\n'.join(lines[:-1]) # Supprimer la dernière ligne
        text_bottom = truncated_text

    # Affichage de l'image de fond
    screen.blit(background_image, (0, 0))

    # Affichage de la barre de navigation
    for i, tab in enumerate(tabs):
        tab_surface = font.render(tab, True, white)
        tab_rect = tab_surface.get_rect()
        tab_rect.topleft = (0, i * tab_height)
        pygame.draw.rect(screen, black, (tab_rect.left, tab_rect.top, tab_width, tab_height))
        text_rect = tab_rect.move(10, (tab_height - font.size(tab)[1]) // 2)
        screen.blit(tab_surface, text_rect)

    # Affichage des rectangles blancs avec coins arrondis
    pygame.draw.rect(screen, white, (rectangle1_x, rectangle1_y, rectangle1_width, rectangle1_height),
                     border_radius=corner_radius)
    pygame.draw.rect(screen, white, (rectangle2_x, rectangle2_y, rectangle2_width, rectangle2_height),
                     border_radius=corner_radius)

    # Affichage du texte et du curseur
    lines_bottom = text_bottom.split('\n')
    for i, line in enumerate(lines_bottom):
        line_surface = font.render(line, True, black)
        screen.blit(line_surface, (rectangle2_x + 10, rectangle2_y + 10 + i * font.get_linesize()))
        if i == len(lines_bottom) - 1:
            # Mise à jour de la position du curseur
            cursor_x = min(rectangle2_x + 10 + font.size(line)[0], rectangle2_x + rectangle2_width - 10)
            cursor_y = min(rectangle2_y + 10 + i * font.get_linesize(),
                           rectangle2_y + rectangle2_height - font.get_height())

    # Affichage du texte dans le rectangle du haut
    screen.blit(text_surface_top, (rectangle1_x + 10, rectangle1_y + 10))

    # Clignotement du curseur
    current_time = pygame.time.get_ticks()
    cursor_blink_interval = 500
    if current_time % cursor_blink_interval < cursor_blink_interval / 2:
        pygame.draw.line(screen, black, (cursor_x, cursor_y), (cursor_x, cursor_y + font.get_height()), 2)

    # Affichage de l'image "send1.png" à la position définie
    screen.blit(send_image, send_image_rect.topleft)

    # Mise à jour de l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()


























































