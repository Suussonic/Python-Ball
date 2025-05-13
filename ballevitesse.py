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

# Coefficient de restitution (pour simuler la perte d'énergie lors du rebond)
coefficient_restitution = 0.9

# Rayon de la balle
rayon_balle = 20

# Rayon du grand cercle blanc (réduit pour entrer dans la fenêtre)
rayon_cercle = 250

# Épaisseur du contour du cercle (pour donner l'effet de cage)
epaisseur_cercle = 10

# Facteur d'accélération à chaque collision
facteur_acceleration = 0.2

# Chargement du son (version Sound pour superposition)
try:
    son_collision = pygame.mixer.Sound("son.mp3")
except pygame.error as e:
    print("Erreur lors du chargement du son :", e)
    son_collision = None

# Variable pour savoir si la balle touche le cercle
touche_cercle = False

# Boucle principale
clock = pygame.time.Clock()
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
    distance_centre = math.hypot(position_balle_x - largeur_fenetre // 2, position_balle_y - hauteur_fenetre // 2)

    # Vérification si la balle touche le cercle
    if distance_centre + rayon_balle >= rayon_cercle:
        if not touche_cercle:  # Si la balle touche le cercle pour la première fois
            touche_cercle = True
            if son_collision:
                son_collision.play()
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

        # Augmentation de la vitesse de la balle pour simuler l'accélération
        vitesse_balle_x *= (1 + facteur_acceleration)
        vitesse_balle_y *= (1 + facteur_acceleration)

    else:
        touche_cercle = False  # Reset pour permettre le son à la prochaine collision

    # Dessin de la balle rouge
    pygame.draw.circle(fenetre, rouge, (int(position_balle_x), int(position_balle_y)), rayon_balle)

    # Mise à jour de l'affichage
    pygame.display.flip()

    # Gestion du framerate (pour limiter la vitesse de la boucle)
    clock.tick(60)

# Fermeture de pygame
pygame.quit()
