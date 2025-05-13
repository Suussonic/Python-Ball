import pygame
import math

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
largeur_fenetre = 800
hauteur_fenetre = 600

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Ball Base")

# Couleurs
noir = (0, 0, 0)
blanc = (255, 255, 255)
rouge = (255, 0, 0)

# Position initiale de la balle
position_balle_x = largeur_fenetre // 4
position_balle_y = hauteur_fenetre // 4

# Vitesse initiale
vitesse_balle_x = 2
vitesse_balle_y = 0

# Gravité et rebond
gravite = 0.5
coefficient_restitution = 0.9

# Dimensions
rayon_balle = 20
rayon_cercle = 250
epaisseur_cercle = 10

# Chargement du son
try:
    son_collision = pygame.mixer.Sound("son.mp3")
except pygame.error as e:
    print("Erreur lors du chargement du son :", e)
    son_collision = None

# Clock
clock = pygame.time.Clock()

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Efface l'écran
    fenetre.fill(noir)

    # Calcul position prévisionnelle
    prochaine_x = position_balle_x + vitesse_balle_x
    prochaine_y = position_balle_y + vitesse_balle_y

    # Vecteur centre -> position prévue
    dx = prochaine_x - largeur_fenetre // 2
    dy = prochaine_y - hauteur_fenetre // 2
    distance_prevue = math.hypot(dx, dy)

    # Collision avec l'intérieur du cercle ?
    if distance_prevue + rayon_balle >= rayon_cercle:
        if son_collision:
            son_collision.play()

        # Normaliser direction du centre vers la balle
        direction_x = dx / distance_prevue
        direction_y = dy / distance_prevue

        # Replace la balle juste à l'intérieur
        position_balle_x = largeur_fenetre // 2 + direction_x * (rayon_cercle - rayon_balle)
        position_balle_y = hauteur_fenetre // 2 + direction_y * (rayon_cercle - rayon_balle)

        # Calcul du rebond par projection vectorielle
        vitesse_normale = direction_x * vitesse_balle_x + direction_y * vitesse_balle_y
        vitesse_balle_x -= (1 + coefficient_restitution) * vitesse_normale * direction_x
        vitesse_balle_y -= (1 + coefficient_restitution) * vitesse_normale * direction_y
    else:
        # Pas de collision
        position_balle_x = prochaine_x
        position_balle_y = prochaine_y

    # Appliquer la gravité
    vitesse_balle_y += gravite

    # Dessin du cercle et de la balle
    pygame.draw.circle(fenetre, blanc, (largeur_fenetre // 2, hauteur_fenetre // 2), rayon_cercle, epaisseur_cercle)
    pygame.draw.circle(fenetre, rouge, (int(position_balle_x), int(position_balle_y)), rayon_balle)

    # Rafraîchissement
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
