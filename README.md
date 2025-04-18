# 🏰 RPG Battle Patata

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Bienvenue dans **RPG Battle Patata**, un mini-jeu de combat RPG en ligne de commande développé avec amour par [LittlePinkSloth](https://github.com/LittlePinkSloth) 🐷✨.

## 🎮 Description

Dans ce jeu, vous incarnez un héros intrépide qui explore un donjon rempli de dangers. Combattez des ennemis générés aléatoirement, gagnez de l'expérience, et survivez le plus longtemps possible !

## ⚔️ Fonctionnalités

- Choix de personnages jouables (avec classes différentes)
- Système de combat tour par tour
- Génération aléatoire d'événements et d'ennemis via des tables de rencontre
- Gain d'expérience et de niveaux
- Statistiques affichées à chaque tour
- Console clear et pause pour une meilleure expérience utilisateur
- Sauvegarde et chargement de personnage
- Texte en couleur pour meilleur confort de jeu
- Ajout de monstres "Elite" et "Boss" pour toujours plus de challenge !
- Ajout d'items suppresseurs de malus

## 🚀 Lancer le jeu

Assurez-vous d'utiliser **Python 3.10+**.  
Clonez le dépôt, installez les dépendances, puis lancez simplement le fichier `main.py` :

```bash
pip install -r requirements.txt
python main.py
```

## 📂 Organisation des fichiers

- `main.py` : point d’entrée du jeu
- `game/` : dossier contenant les modules suivants :
  - `characters.py` : classes des personnages
  - `items.py` : objets utilisables
  - `events.py` : génération d'événements et logique de combat
  - `data.py` : données statiques

## 📦 Dépendances

- `random`
- `msvcrt`
- `os`
- `genericpath`

Dépendance externe :
- `colorama`

## What to expect in next updates ?
- Malus (poison, aveuglement, brûlure...)
- Endroits magiques
- Buffs
- Nouveaux ennemis
- Nouvelles classes de personnage
- Possibilité de jeter ses objets


## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'infos.

---

✨ Amusez-vous bien, et attention aux patatas sauvages !
