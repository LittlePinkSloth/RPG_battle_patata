# 🏰 RPG Battle Patata

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Bienvenue dans **RPG Battle Patata**, un mini-jeu de combat RPG en ligne de commande développé avec amour par [LittlePinkSloth](https://github.com/LittlePinkSloth) 🐷✨.

## 🎮 Description

Dans ce jeu, vous incarnez un héros intrépide qui explore un donjon rempli de dangers. Combattez des ennemis générés aléatoirement, gérez vos objets et vos statistiques, et survivez le plus longtemps possible !

## ⚔️ Fonctionnalités

- Choix de personnages jouables avec des classes différentes
- Système de combat tour par tour
- Génération aléatoire d'événements, ennemis et objets via des tables JSON
- Apparition de Boss et d'Elites
- Effets de statut (brûlure, poison...) et objets pour les soigner
- Système d'inventaire et d’équipement
- Sauvegarde et chargement de partie
- Console colorée (via `colorama`) et clear/pause pour une meilleure lisibilité
- Structure de projet modulaire pour une meilleure lisibilité et évolutivité
- Plusieurs langues disponibles : Français, anglais et espagnol

## 🚀 Lancer le jeu
### Prérequis 
Assurez-vous d’utiliser **Python 3.10+**.

### Installation
Clonez le dépôt :
```bash
git clone https://github.com/LittlePinkSloth/RPG_battle_patata.git
cd RPG_battle_patata
```
Installez les dépendances :
```bash
pip install -r requirements.txt
```

### Exécution
Depuis le dossier contenant le projet (donc avant le dossier RPG_battle_patata) :
```bash
python -m RPG_battle_patata
```

## 📂 Structure du projet

```
RPG_battle_patata/
├── __main__.py          # Lancement du jeu via `python -m RPG_battle_patata`
├── main.py              # Entrée principale (appelée par __main__)
├── requirements.txt
├── README.md
├── LICENSE
│
├── data/                    # Données statiques JSON et ambiance
│   ├── ENEMY_TABLE.json
│   ├── EVENT_TABLE.json
│   ├── ITEM_TABLE.json
│   ├── STATUS_TABLE.json
│   ├── text_english.json
│   ├── text_french.json
│   └── text_spanish.json
│
├── entities/                # Définition des entités du jeu
│   ├── characters.py        # Joueur, classes...
│   ├── eny.py               # Ennemis
│   ├── rpg_exceptions.py    # Gestion des erreurs spécifiques
│   └── items.py             # Objets, équipements, effets
│
├── game/                    # Logique du jeu
│   ├── events.py            # Gestion des événements et combats
│   ├── engine.py            # Gestion du moteur du jeu
│   ├── display.py           # Fonctions d'affichage
│   ├── language_manager.py  # Gestion des langues
│   └── utils.py             # Outils divers (clear screen, couleurs, etc)
│
├── save/                    # Dossier pour les sauvegardes
```

## 📦 Dépendances

- `random`, `os`, `msvcrt` (standard Python)
- `colorama` (console colorée)

Installez-les via le `requirements.txt` fourni.

## 🔮 À venir

- Nouvelles classes de personnages
- Buffs et malus variés (aveuglement, confusion...)
- Lieux spéciaux (magiques ou piégés)
- Possibilité de jeter ou trier les objets
- Système de quêtes aléatoires

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'infos.

---

✨ Amusez-vous bien, et attention aux patatas sauvages !