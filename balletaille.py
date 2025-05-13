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

# Position initiale
position_balle_x = largeur_fenetre // 4
position_balle_y = hauteur_fenetre // 4

# Vitesse initiale
vitesse_balle_x = 2
vitesse_balle_y = 0

# Gravité et rebond
gravite = 0.5
coefficient_restitution = 0.9

# Rayons
rayon_balle = 20
rayon_cercle = 250
epaisseur_cercle = 10
facteur_agrandissement = 1

# Chargement du son (version Sound)
try:
    son_collision = pygame.mixer.Sound("son.mp3")
except pygame.error as e:
    print("Erreur lors du chargement du son :", e)
    son_collision = None

# Variable de contact
touche_cercle = False

# Boucle principale
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    fenetre.fill(noir)

    # Mise à jour position
    position_balle_x += vitesse_balle_x
    position_balle_y += vitesse_balle_y

    # Gravité
    vitesse_balle_y += gravite

    # Dessin du cercle
    pygame.draw.circle(fenetre, blanc, (largeur_fenetre // 2, hauteur_fenetre // 2), rayon_cercle, epaisseur_cercle)

    # Distance centre
    distance_centre = math.hypot(position_balle_x - largeur_fenetre // 2,
                                 position_balle_y - hauteur_fenetre // 2)

    # Collision ?
    if distance_centre + rayon_balle >= rayon_cercle:
        if not touche_cercle:
            touche_cercle = True
            if son_collision:
                son_collision.play()

        # Calcul de l’angle
        angle = math.atan2(position_balle_y - hauteur_fenetre // 2,
                           position_balle_x - largeur_fenetre // 2)

        # Correction de la position
        position_balle_x = largeur_fenetre // 2 + math.cos(angle) * (rayon_cercle - rayon_balle)
        position_balle_y = hauteur_fenetre // 2 + math.sin(angle) * (rayon_cercle - rayon_balle)

        # Rebond
        vitesse_normale_x = math.cos(angle) * vitesse_balle_x + math.sin(angle) * vitesse_balle_y
        vitesse_normale_y = -math.sin(angle) * vitesse_balle_x + math.cos(angle) * vitesse_balle_y

        vitesse_normale_x = -vitesse_normale_x * coefficient_restitution
        vitesse_normale_y = vitesse_normale_y * coefficient_restitution

        vitesse_balle_x = math.cos(angle) * vitesse_normale_x - math.sin(angle) * vitesse_normale_y
        vitesse_balle_y = math.sin(angle) * vitesse_normale_x + math.cos(angle) * vitesse_normale_y

        # Agrandissement
        rayon_balle += facteur_agrandissement

    else:
        touche_cercle = False  # Reset pour permettre le son à la prochaine collision

    # Dessin balle
    pygame.draw.circle(fenetre, rouge, (int(position_balle_x), int(position_balle_y)), rayon_balle)

    # Rafraîchissement
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
