import pygame
import math

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
largeur_fenetre = 800
hauteur_fenetre = 600

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Single Mur")

# Couleurs
noir  = (0, 0, 0)
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
rayon_balle   = 20
rayon_cercle  = 250
epaisseur_cercle = 10

# Paramètres du trou
angle_trou      = 0                    # angle de départ du trou (en radians)
largeur_trou    = math.radians(60)     # largeur du trou (~60°)
vitesse_rotation = math.radians(1.5)   # vitesse de rotation du mur (radians par frame)

# Chargement du son
try:
    son_collision = pygame.mixer.Sound("son.mp3")
except pygame.error as e:
    print("Erreur lors du chargement du son :", e)
    son_collision = None

# Clock
clock = pygame.time.Clock()

balle_sortie = False  # État pour savoir si la balle est sortie du mur

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    fenetre.fill(noir)
    angle_trou = (angle_trou + vitesse_rotation) % (2 * math.pi)

    # Calcul de la prochaine position de la balle
    prochaine_x = position_balle_x + vitesse_balle_x
    prochaine_y = position_balle_y + vitesse_balle_y

    # Distance et angle de la balle par rapport au centre
    dx = prochaine_x - largeur_fenetre // 2
    dy = prochaine_y - hauteur_fenetre // 2
    distance_prevue = math.hypot(dx, dy)

    # *Correction ici* : on inverse dy pour que l'angle soit dans le même référentiel que pygame.draw.arc
    angle_balle = math.atan2(-dy, dx) % (2 * math.pi)
    angle_debut_trou = angle_trou % (2 * math.pi)
    angle_fin_trou   = (angle_trou + largeur_trou) % (2 * math.pi)

    def angle_dans_trou(angle, debut, fin):
        if debut < fin:
            return debut <= angle <= fin
        else:
            return angle >= debut or angle <= fin

    if not balle_sortie:
        # Collision avec le mur (sauf si la balle est dans le trou)
        if distance_prevue + rayon_balle >= rayon_cercle:
            if angle_dans_trou(angle_balle, angle_debut_trou, angle_fin_trou):
                # La balle sort par le trou
                balle_sortie = True
                position_balle_x = prochaine_x
                position_balle_y = prochaine_y
            else:
                # Rebond sur le mur
                if son_collision:
                    son_collision.play()
                direction_x = dx / distance_prevue
                direction_y = dy / distance_prevue
                position_balle_x = largeur_fenetre // 2 + direction_x * (rayon_cercle - rayon_balle)
                position_balle_y = hauteur_fenetre // 2 + direction_y * (rayon_cercle - rayon_balle)
                vitesse_normale = direction_x * vitesse_balle_x + direction_y * vitesse_balle_y
                vitesse_balle_x -= (1 + coefficient_restitution) * vitesse_normale * direction_x
                vitesse_balle_y -= (1 + coefficient_restitution) * vitesse_normale * direction_y
        else:
            # Pas de collision, la balle continue
            position_balle_x = prochaine_x
            position_balle_y = prochaine_y
    else:
        # La balle est déjà sortie, elle tombe librement
        position_balle_x = prochaine_x
        position_balle_y = prochaine_y

    # Appliquer la gravité
    vitesse_balle_y += gravite

    # *** Plus de décalage angulaire nécessaire pour le rendu ***
    angle_debut_trou_draw = angle_debut_trou
    angle_fin_trou_draw   = angle_fin_trou

    # Dessin du mur circulaire (deux arcs blancs laissés vides pour représenter le trou)
    rect_cercle = pygame.Rect(
        largeur_fenetre // 2 - rayon_cercle,
        hauteur_fenetre // 2 - rayon_cercle,
        rayon_cercle * 2,
        rayon_cercle * 2
    )
    if angle_debut_trou_draw < angle_fin_trou_draw:
        pygame.draw.arc(fenetre, blanc, rect_cercle, 0, angle_debut_trou_draw, epaisseur_cercle)
        pygame.draw.arc(fenetre, blanc, rect_cercle, angle_fin_trou_draw, 2 * math.pi, epaisseur_cercle)
    else:
        pygame.draw.arc(fenetre, blanc, rect_cercle, angle_fin_trou_draw, angle_debut_trou_draw, epaisseur_cercle)

    # Dessin de la balle
    pygame.draw.circle(fenetre, rouge, (int(position_balle_x), int(position_balle_y)), rayon_balle)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
