# Python-Ball

Projet d’animations de balles en Python, pour explorer la physique, les collisions et les effets visuels avec Pygame.

## 📜 Sommaire

- [Ball Base](#🏀-ballbase)
- [Ball Vitesse](#🏃-ballevitesse)
- [Ball Taille](#🔼-balltaille)
- [Ball Couleur](#🤹-ballcouleur)
- [Mur](#🕳️-mur)
- [Effets sonores](#🔊-effets-sonores)
- [Personnalisation](#🎨-personnalisation)
- [Lancer les scripts](#▶️-lancer-les-scripts)

---

## 🏀 BallBase

Programme de base d'une balle rebondissante dans un cercle.

## 🏃 BallVitesse

A chaque Rebond la vitesse de la balle accélére.

## 🔼 BallTaille

A chaque Rebond la vitesse de la balle grandi.

## 🤹 BallCouleur

A chaque Rebond la vitesse de la balle change de couleur.

## 🕳️ Mur

La balle rebondit à l’intérieur d’un cercle. Un trou rotatif permet à la balle de s’échapper si elle passe au bon endroit.  

## 🔊 Effets sonores

À chaque collision avec le mur, un son est joué (fichier `son.mp3` requis dans le dossier du script).

## 🎨 Personnalisation

Vous pouvez modifier :
- La taille de la fenêtre (`largeur_fenetre`, `hauteur_fenetre`)
- La gravité (`gravite`)
- Le coefficient de restitution (`coefficient_restitution`)
- La taille du trou (`largeur_trou`)
- La vitesse de rotation du mur (`vitesse_rotation`)
- Les couleurs et tailles des éléments

## ▶️ Lancer les scripts

Assurez-vous d’avoir Python et Pygame installés :

```bash
pip install pygame
```
