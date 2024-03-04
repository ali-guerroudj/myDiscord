import pygame
import mysql.connector
from mysql.connector import connect, Error

class Inscription:
    def __init__(self):
        # Initialisation de Pygame
        pygame.init()

        # Définition des couleurs
        self.BLEU = (0, 0, 255)
        self.BLANC = (255, 255, 255)
        self.NOIR = (0, 0, 0)
        self.violetred4 = (139, 34, 82, 255)

        # Définition de la résolution de la fenêtre
        self.res = (940, 800)

        # Création de la fenêtre
        self.window_surface = pygame.display.set_mode(self.res)
        pygame.display.set_caption("Fenêtre d'inscription")

        # Police de texte avec une taille spécifique
        self.font = pygame.font.SysFont(None, 36)

        # Charger l'image d'arrière-plan
        self.bg_image = pygame.image.load('image/bc1.png')

        # Redimensionner l'image pour qu'elle corresponde à la résolution de la fenêtre
        self.bg_image = pygame.transform.scale(self.bg_image, self.res)

        # Position et dimension du carré de connexion
        self.carré_x = 200
        self.carré_y = 200
        self.carré_largeur = 500
        self.carré_hauteur = 500

        # Variables pour stocker le contenu des champs de saisie
        self.first_name_text = ""
        self.last_name_text = ""
        self.email_text = ""
        self.mdp_text = ""

        # Variable pour suivre le champ actif
        self.active_field = None

        # Définir le temps de clignotement du curseur en millisecondes
        self.BLINK_TIME = 500  # 500 ms

        # Définir le temps du dernier clignotement
        self.last_blink = pygame.time.get_ticks()

        # Indicateur pour savoir si le curseur est visible
        self.cursor_visible = False

        # Définition des propriétés du bouton
        self.bouton_x = 300
        self.bouton_y = 450
        self.bouton_largeur = 200
        self.bouton_hauteur = 50
        self.couleur_bouton_normal = (50, 205, 50)  # Vert
        self.couleur_bouton_survol = (0, 255, 0)     # Vert clair

    # Fonction pour établir la connexion à la base de données
    def connecter_bdd(self):
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
    def inserer_utilisateur(self, conn, first_name, last_name, email, password):
        try:
            cursor = conn.cursor()
            insert_query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
            values = (first_name, last_name, email, password)
            cursor.execute(insert_query, values)
            conn.commit()
            print("Utilisateur inséré avec succès !")
        except Error as e:
            print(f"Erreur lors de l'insertion de l'utilisateur dans la base de données: {e}")

    # Fonction principale pour exécuter l'inscription
    def run(self):
        # Boucle principale du jeu
        launched = True
        while launched:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    launched = False
                elif event.type == pygame.KEYDOWN:
                    if self.active_field == 'first_name':
                        if event.key == pygame.K_BACKSPACE:
                            self.first_name_text = self.first_name_text[:-1]  # Supprimer le dernier caractère
                        elif len(self.first_name_text) < 50:
                            self.first_name_text += event.unicode
                    elif self.active_field == 'last_name':
                        if event.key == pygame.K_BACKSPACE:
                            self.last_name_text = self.last_name_text[:-1]  # Supprimer le dernier caractère
                        elif len(self.last_name_text) < 50:
                            self.last_name_text += event.unicode
                    elif self.active_field == 'email':
                        if event.key == pygame.K_BACKSPACE:
                            self.email_text = self.email_text[:-1]  # Supprimer le dernier caractère
                        elif len(self.email_text) < 100:
                            self.email_text += event.unicode
                    elif self.active_field == 'password':
                        if event.key == pygame.K_BACKSPACE:
                            self.mdp_text = self.mdp_text[:-1]  # Supprimer le dernier caractère
                        elif len(self.mdp_text) < 100:
                            self.mdp_text += event.unicode

                # Gérer le focus sur les champs de saisie
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    first_name_rect = pygame.Rect(self.carré_x + 100, self.carré_y + 40, 200, 30)
                    last_name_rect = pygame.Rect(self.carré_x + 100, self.carré_y + 100, 200, 30)
                    email_rect = pygame.Rect(self.carré_x + 100, self.carré_y + 160, 200, 30)
                    password_rect = pygame.Rect(self.carré_x + 100, self.carré_y + 220, 200, 30)
                    if first_name_rect.collidepoint(event.pos):
                        self.active_field = 'first_name'
                    elif last_name_rect.collidepoint(event.pos):
                        self.active_field = 'last_name'
                    elif email_rect.collidepoint(event.pos):
                        self.active_field = 'email'
                    elif password_rect.collidepoint(event.pos):
                        self.active_field = 'password'
                    else:
                        self.active_field = None
                        
                    # Vérifier si la souris est cliquée sur le bouton de connexion
                    if self.bouton_x < event.pos[0] < self.bouton_x + self.bouton_largeur and self.bouton_y < event.pos[1] < self.bouton_y + self.bouton_hauteur:
                        print("Bouton de connexion cliqué !")  # Ici, vous pouvez ajouter votre logique de connexion
                        
                        # Établir une connexion à la base de données
                        conn = self.connecter_bdd()
                        if conn:
                            # Insérer l'utilisateur dans la base de données
                            self.inserer_utilisateur(conn, self.first_name_text, self.last_name_text, self.email_text, self.mdp_text)
                            # Fermer la connexion
                            conn.close()

            # Effacer l'écran
            self.window_surface.fill(self.BLANC)

            # Dessiner l'image d'arrière-plan redimensionnée
            self.window_surface.blit(self.bg_image, (0, 0))

            # Afficher le carré de connexion
            pygame.draw.rect(self.window_surface, self.violetred4, (self.carré_x, self.carré_y, self.carré_largeur, self.carré_hauteur))
            text_connexion = self.font.render("Inscription", True, self.BLANC)
            self.window_surface.blit(text_connexion, (self.carré_x + 50, self.carré_y + 10))

            # Afficher les champs de saisie avec le texte saisi
            pygame.draw.rect(self.window_surface, self.NOIR, (self.carré_x + 100, self.carré_y + 40, 200, 30), 2)  # Champ Prénom
            pygame.draw.rect(self.window_surface, self.NOIR, (self.carré_x + 100, self.carré_y + 100, 200, 30), 2)  # Champ Nom
            pygame.draw.rect(self.window_surface, self.NOIR, (self.carré_x + 100, self.carré_y + 160, 200, 30), 2)  # Champ E-mail
            pygame.draw.rect(self.window_surface, self.NOIR, (self.carré_x + 100, self.carré_y + 220, 200, 30), 2)  # Champ Mot de passe

            # Afficher le texte saisi dans le champ actif
            first_name_surface = self.font.render(self.first_name_text, True, self.NOIR)
            self.window_surface.blit(first_name_surface, (self.carré_x + 105, self.carré_y + 45))

            last_name_surface = self.font.render(self.last_name_text, True, self.NOIR)
            self.window_surface.blit(last_name_surface, (self.carré_x + 105, self.carré_y + 105))

            email_surface = self.font.render(self.email_text, True, self.NOIR)
            self.window_surface.blit(email_surface, (self.carré_x + 105, self.carré_y + 165))

            mdp_surface = self.font.render("*" * len(self.mdp_text), True, self.NOIR)  # Pour masquer le mot de passe
            self.window_surface.blit(mdp_surface, (self.carré_x + 105, self.carré_y + 225))

            # Afficher les labels des champs
            first_name_label = self.font.render("Prénom:", True, self.NOIR)
            self.window_surface.blit(first_name_label, (self.carré_x + 50, self.carré_y + 10))
            last_name_label = self.font.render("Nom:", True, self.NOIR)
            self.window_surface.blit(last_name_label, (self.carré_x + 50, self.carré_y + 70))
            email_label = self.font.render("E-mail:", True, self.NOIR)
            self.window_surface.blit(email_label, (self.carré_x + 50, self.carré_y + 130))
            mdp_label = self.font.render("Mot de passe:", True, self.NOIR)
            self.window_surface.blit(mdp_label, (self.carré_x + 50, self.carré_y + 190))

            # Dessiner le bouton de connexion
            pygame.draw.rect(self.window_surface, self.couleur_bouton_normal, (self.bouton_x, self.bouton_y, self.bouton_largeur, self.bouton_hauteur))
            text_bouton = self.font.render("Connexion", True, self.BLANC)
            self.window_surface.blit(text_bouton, (self.bouton_x + 50, self.bouton_y + 15))

            # Actualiser l'affichage
            pygame.display.flip()

        # Quitter Pygame
        pygame.quit()

# Créer une instance de la classe et exécuter le programme
if __name__ == "__main__":
    app = Inscription()
    app.run()









