import pygame
import math

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
largeur_fenetre = 800
hauteur_fenetre = 600

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Balle et Gravité")

# Couleurs
noir = (0, 0, 0)
blanc = (255, 255, 255)
rouge = (255, 0, 0)

# Position initiale de la balle (non centrée)
position_balle_x = largeur_fenetre // 4
position_balle_y = hauteur_fenetre // 4

# Vitesse initiale de la balle
vitesse_balle_x = 2  # Vitesse horizontale initiale
vitesse_balle_y = 0  # Vitesse verticale initiale

# Accélération due à la gravité
gravite = 0.5

# Rayon initial de la balle
rayon_balle = 20

# Rayon du grand cercle blanc (réduit pour entrer dans la fenêtre)
rayon_cercle = 250

# Épaisseur du contour du cercle (pour donner l'effet de cage)
epaisseur_cercle = 10

# Facteur d'augmentation du rayon de la balle à chaque collision
facteur_agrandissement = 5

# Chargement du son
try:
    pygame.mixer.music.load("son.mp3")  # Utilisation de pygame.mixer.music pour des morceaux longs
except pygame.error as e:
    print("Erreur lors du chargement du son :", e)
    pygame.mixer.music = None  # Assurez-vous que le programme continue même si le son ne peut pas être chargé

# Variables pour la gestion du son
duree_minimale_son = 1000  # Durée minimale du son en millisecondes
derniere_collision = 0  # Temps de la dernière collision
son_joue = False  # Pour vérifier si le son est actuellement joué

# Variable pour savoir si la balle touche le cercle
touche_cercle = False

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Si on ferme la fenêtre
            running = False

    # Remplir l'écran avec une couleur noire
    fenetre.fill(noir)

    # Calcul de la position de la balle
    position_balle_x += vitesse_balle_x
    position_balle_y += vitesse_balle_y

    # Ajout de l'effet de la gravité sur la balle
    vitesse_balle_y += gravite

    # Dessin du grand cercle blanc au centre de la fenêtre
    pygame.draw.circle(fenetre, blanc, (largeur_fenetre // 2, hauteur_fenetre // 2), rayon_cercle, epaisseur_cercle)

    # Calcul de la distance entre la balle et le centre du cercle
    distance_centre = math.sqrt((position_balle_x - largeur_fenetre // 2) ** 2 + (position_balle_y - hauteur_fenetre // 2) ** 2)

    # Vérification si la balle touche le cercle
    if distance_centre + rayon_balle >= rayon_cercle:
        if not touche_cercle:  # Si la balle touche le cercle pour la première fois
            touche_cercle = True
            derniere_collision = pygame.time.get_ticks()  # Enregistrer le temps de la collision
            if pygame.mixer.music and not pygame.mixer.music.get_busy():  # Si le son n'est pas déjà joué
                pygame.mixer.music.play(-1)  # Lecture du son en boucle (indéfini)

        # Calcul de l'angle de collision
        angle = math.atan2(position_balle_y - hauteur_fenetre // 2, position_balle_x - largeur_fenetre // 2)

        # Correction de la position pour éviter que la balle ne pénètre le cercle
        position_balle_x = largeur_fenetre // 2 + math.cos(angle) * (rayon_cercle - rayon_balle)
        position_balle_y = hauteur_fenetre // 2 + math.sin(angle) * (rayon_cercle - rayon_balle)

        # Calcul de la vitesse après le rebond (inversion par rapport à la normale)
        vitesse_normale_x = math.cos(angle) * vitesse_balle_x + math.sin(angle) * vitesse_balle_y
        vitesse_normale_y = -math.sin(angle) * vitesse_balle_x + math.cos(angle) * vitesse_balle_y

        vitesse_normale_x = -vitesse_normale_x * coefficient_restitution
        vitesse_normale_y = vitesse_normale_y * coefficient_restitution

        vitesse_balle_x = math.cos(angle) * vitesse_normale_x - math.sin(angle) * vitesse_normale_y
        vitesse_balle_y = math.sin(angle) * vitesse_normale_x + math.cos(angle) * vitesse_normale_y

        # Augmentation du rayon de la balle pour simuler la croissance
        rayon_balle += facteur_agrandissement

    else:
        if touche_cercle and pygame.mixer.music.get_busy():  # Si la balle ne touche plus le cercle et la musique joue
            temps_ecoule = pygame.time.get_ticks() - derniere_collision
            if temps_ecoule >= duree_minimale_son:
                pygame.mixer.music.stop()  # Arrêt du son après la durée minimale
                touche_cercle = False

    # Dessin de la balle rouge
    pygame.draw.circle(fenetre, rouge, (int(position_balle_x), int(position_balle_y)), rayon_balle)

    # Mise à jour de l'affichage
    pygame.display.flip()

    # Gestion du framerate (pour limiter la vitesse de la boucle)
    pygame.time.Clock().tick(60)

# Fermeture de pygame
pygame.quit()
