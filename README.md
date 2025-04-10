# 🏰 RPG Battle Patata

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Bienvenue dans **RPG Battle Patata**, un mini-jeu de combat RPG en ligne de commande développé avec amour par [LittlePinkSloth](https://github.com/LittlePinkSloth) 🐷✨.

## 🎮 Description

Dans ce jeu, vous incarnez un héros intrépide qui explore un donjon rempli de dangers. Combattez des ennemis générés aléatoirement, gagnez de l'expérience, et survivez le plus longtemps possible !

## ⚔️ Fonctionnalités

- Choix de personnages jouables (avec classes différentes)
- Système de combat tour par tour
- Génération aléatoire d'événements et d'ennemis
- Gain d'expérience
- Statistiques affichées à chaque tour
- Console clear et pause pour une meilleure expérience utilisateur

## 🚀 Lancer le jeu

Assurez-vous d'utiliser **Python 3.10+**.  
Clonez le dépôt puis lancez simplement le fichier `main.py` :

```bash
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

Pas de dépendance externe ! Le jeu utilise uniquement :  
- `random`
- `msvcrt`
- `os`

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'infos.

---

✨ Amusez-vous bien, et attention aux patatas sauvages !
