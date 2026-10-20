# Le Manoir des Ombres

[![Build Ren'Py Web](https://github.com/ElPistone/Manoir_Des_Ombres/actions/workflows/build_web.yml/badge.svg)](https://github.com/ElPistone/Manoir_Des_Ombres/actions/workflows/build_web.yml)

[Lien vers la démo](https://elpistone.github.io/Manoir_Des_Ombres/)

Jeu narratif développé avec **Ren'Py**, mêlant exploration, énigmes et un système de pari sur un inventaire de fragments de carte. Perdu de nuit, le joueur trouve refuge dans un manoir qui se révèle être un labyrinthe : pour en sortir, il doit reconstituer une carte complète en traversant une série de portes, chacune gardée par une énigme.
> Projet en développement actif (Master PSM).

---

## Sommaire

- [Synopsis](#synopsis)
- [Mécanique de jeu](#mécanique-de-jeu)
- [Prérequis](#prérequis)
- [Installation et lancement](#installation-et-lancement)
- [Structure du projet](#structure-du-projet)
- [Pipeline de production des assets](#pipeline-de-production-des-assets)
- [État actuel et limitations connues](#état-actuel-et-limitations-connues)
- [Roadmap](#roadmap)
- [Outils et crédits](#outils-et-crédits)
- [Licence](#licence)

---

## Synopsis

Une nuit, perdu en pleine forêt sous l'orage, le joueur trouve refuge dans un vieux manoir. Mais le bâtiment est un labyrinthe : chaque pièce dissimule une porte gardant une énigme. Pour retrouver la sortie, il doit reconstituer une carte complète en traversant ces portes, au péril des fragments de carte qu'il possède déjà.

Direction artistique : nuit mystérieuse, manoir gothique, parchemin et encre dorée, aquarelle sombre. Palette resserrée : bleu nuit, sépia, or vieilli, vert sombre, bordeaux. Aucun personnage, visage ou main représenté, pour conserver une ambiguïté inquiétante.

## Mécanique de jeu

- Le joueur commence avec **1 fragment de carte** (trouvé dans le hall d'entrée).
- Le manoir compte **9 portes**, chacune gardée par une énigme à choix multiples.
- Avant chaque porte, le joueur **mise un fragment de carte** qu'il possède.
  - **Bonne réponse** → il récupère son fragment **et** en gagne un nouveau.
  - **Mauvaise réponse** → le fragment misé est perdu définitivement, mais la partie continue.
- **Victoire** : les 10 fragments sont réunis (le fragment de départ + les 9 obtenus aux portes).
- **Défaite** : le joueur n'a plus aucun fragment à miser.
- Un écran dédié (« la carte ») permet de visualiser la reconstitution de la carte au fil de la partie.

## Prérequis

- [Ren'Py SDK](https://www.renpy.org/) **8.5.3** ou version compatible (le projet a été testé sur cette version ; certaines variables de configuration diffèrent selon les versions, voir [État actuel](#état-actuel-et-limitations-connues))
- Python 3 (fourni avec le SDK Ren'Py, pas d'installation séparée nécessaire pour lancer le jeu)
- Pour les scripts de production d'assets uniquement : Python 3 + [Pillow](https://pypi.org/project/Pillow/) (`pip install pillow`)

## Installation et lancement

1. Installer le [Ren'Py SDK](https://www.renpy.org/latest.html).
2. Placer le dossier `game/` de ce projet dans un nouveau projet Ren'Py (ou l'utiliser comme dossier de projet directement, à la racine duquel se trouve `game/`).
3. Lancer le SDK Ren'Py, sélectionner le projet, cliquer sur **Lancer le projet**.
4. Pour un export final (Windows/Mac/Linux), utiliser **Construire des packages distribuables** depuis le lanceur Ren'Py.

## Structure du projet

```
le-manoir-des-ombres/
├── game/
│   ├── images/
│   │   ├── ui/            # boutons, cadres, icônes, curseur
│   │   ├── backgrounds/    # fonds de chaque salle
│   │   ├── riddles/        # illustrations d'énigmes
│   │   └── map/            # carte complète + fragments découpés
│   ├── audio/               # musiques et bruitages (à venir)
│   ├── variables.rpy        # état global, données des 9 énigmes
│   ├── script.rpy           # boucle de jeu, intro, fins
│   ├── screens.rpy          # écrans : titre, dialogue, énigme, HUD, sauvegarde
│   ├── ui_style.rpy         # palette, bascule interface dessinée/PNG, mise à l'échelle des fonds
│   ├── textes.rpy           # banques de dialogues variés (ambiance, mise, victoire, défaite)
│   └── options.rpy          # configuration du projet
├── decoupage_carte.py        # script Pillow : découpe la carte complète en fragments
├── nettoyer_assets.py        # script Pillow : nettoie les images IA (damier, recadrage)
└── README.md
```

## Pipeline de production des assets

La direction artistique est produite par génération d'images IA, puis retravaillée par deux scripts Python :

1. **`decoupage_carte.py`** — découpe `map_full.png` en fragments (`piece_01.png` à `piece_10.png`) et génère `positions_carte.rpy`, utilisé par l'écran de reconstitution de la carte.
2. **`nettoyer_assets.py`** — les générateurs d'images IA simulent souvent la transparence par un damier gris/blanc au lieu d'un vrai canal alpha, et regroupent parfois plusieurs états d'un bouton (normal/survolé) sur une seule image. Ce script détecte et retire le damier, recadre l'élément utile, et sépare les visuels assemblés. Les originaux sont sauvegardés avant modification.

```bash
pip install pillow
python decoupage_carte.py
python nettoyer_assets.py game/images/ui
```

## État actuel et limitations connues

- **Interface dessinée par défaut** : `ui_style.rpy` a `gm_art_ui = False`, donc le jeu utilise des boutons et cadres unis générés par Ren'Py plutôt que les PNG de `images/ui/`. Passer cette variable à `True` une fois les images nettoyées via `nettoyer_assets.py`.
- **Icônes non câblées** : `icon_map_piece.png` et `icon_score.png` ne sont pour l'instant pas utilisées dans le HUD ni les écrans de jeu (remplacées par des couleurs unies). `cursor.png` n'est pas encore défini comme curseur personnalisé dans `options.rpy`.
- **Nom du jeu** : `config.name` dans `options.rpy` affiche encore « Le Manoir-Labyrinthe » et doit être mis à jour en « Le Manoir des Ombres » pour correspondre au titre actuel.
- **Audio** : aucune musique ni bruitage intégré pour l'instant (`config.main_menu_music` est commenté dans `options.rpy` en attendant les fichiers).
- **Énigmes fixes** : les 9 énigmes et leurs réponses sont codées en dur dans `variables.rpy`, sans tirage aléatoire ni variante.

## Roadmap

- [ ] Câbler `icon_map_piece.png`, `icon_score.png` et `cursor.png`
- [ ] Basculer `gm_art_ui` sur `True` une fois les assets nettoyés
- [ ] Mettre à jour `config.name` dans `options.rpy`
- [ ] Intégrer musique d'ambiance et bruitages (portes, bonne/mauvaise réponse)
- [ ] Finaliser l'ensemble des illustrations (fonds, icônes d'énigmes)

## Outils et crédits

- Moteur de jeu : [Ren'Py](https://www.renpy.org/) (Python)
- Traitement d'images : [Pillow](https://python-pillow.org/)
- Direction artistique : génération d'images IA (prompts sur mesure, cf. documentation de production), retravaillées via scripts maison
- Développement : Diaby Mamadou Dian
