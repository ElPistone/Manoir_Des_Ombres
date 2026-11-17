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

- Le joueur commence avec **1 fragment de carte**, ramassé sous le tapis du hall d'entrée.
- À chaque porte, il **mise un des fragments** qu'il possède, puis répond à une énigme (tirée au hasard, réponses mélangées, sans répétition tant que possible).
  - **Bonne réponse** → il récupère son fragment **et** en gagne un nouveau (tiré au hasard parmi ceux qui manquent).
  - **Mauvaise réponse** → le fragment misé est englouti, mais la partie continue tant qu'il lui en reste. La bonne réponse n'est pas révélée.
- **Chaque fragment a un pouvoir**, actif tant qu'on le possède. Le fragment misé reste sous la porte : **son pouvoir ne joue pas pour cette énigme**. Choisir quoi miser est donc un vrai choix.

  | Fragment | Pouvoir |
  |---|---|
  | Lanterne | La voix souffle un indice |
  | Encre | Une mauvaise réponse est barrée (ou la première lettre révélée) |
  | Sablier | Une fois par porte, on peut demander une autre énigme |
  | Clé | Une fois par partie, une erreur ne coûte rien |

- **Double mise** : avec 2 fragments, on peut tout risquer. L'énigme est plus dure, mais une bonne réponse rapporte 2 fragments d'un coup ; une erreur fait perdre les deux.
- **La difficulté suit le nombre de fragments** : 1 fragment → niveau 0 (très simple, car une erreur fait perdre) ; 2 → niveau 1 ; 3 → niveau 2.
- **Porte de sortie** : une fois la carte complète (4 fragments), il reste à franchir la sortie, gardée par une énigme à **réponse libre** au clavier (niveau 3). Une erreur coûte encore un fragment.
- **Défaite** : plus aucun fragment à miser, ou **12 portes** passées sans être sorti.
- Pas de retour en arrière : une réponse est définitive. Le menu est bloqué pendant la mise et l'énigme, et le manoir **mémorise chaque verdict** : recharger une sauvegarde devant une porte déjà répondue rejoue le même verdict.
- **4 fins** : « La délivrance » (sortir sans aucune erreur), « L'aube » (sortir), « Les mains vides » et « Le dernier coup de minuit » (défaites). Les fins découvertes s'affichent sur l'écran titre.
- **Histoire** : le dos de chaque fragment porte une note d'Edmund ou d'Éléonore Blackwood. On les relit dans l'écran de la carte.
- Entre deux portes, le joueur traverse une pièce du manoir (grenier, cave, escalier, couloirs).

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
│   │   ├── ui/            # cadres, logo, icônes détourées (.webp)
│   │   ├── backgrounds/    # fonds de chaque salle
│   │   ├── riddles/        # illustrations d'énigmes (enigme_*.webp)
│   │   └── map/            # fragments découpés
│   ├── audio/               # musiques et bruitages (synthétisés)
│   ├── fonts/               # Crimson Text et IM Fell English SC (licence OFL)
│   ├── gui/                 # icône de fenêtre, curseur
│   ├── variables.rpy        # règles, fragments et pouvoirs, énigmes, fins
│   ├── positions_carte.rpy  # généré par decoupage_carte.py
│   ├── script.rpy           # boucle de jeu, intro, fins
│   ├── screens.rpy          # écrans : titre, dialogue, énigme, HUD, sauvegarde
│   ├── ui_style.rpy         # palette, bascule interface dessinée/PNG, mise à l'échelle des fonds
│   ├── textes.rpy           # banques de dialogues variés et pièces traversées
│   ├── effets.rpy           # transitions et animations
│   └── options.rpy          # configuration du projet
├── decoupage_carte.py        # script Pillow : découpe la carte complète en fragments
├── outils/nettoyer_assets.py # script Pillow : nettoie les images IA (damier, recadrage)
└── README.md
```

## Pipeline de production des assets

La direction artistique est produite par génération d'images IA, puis retravaillée par deux scripts Python :

1. **`decoupage_carte.py`** — découpe `map_full.png` en 4 fragments (`piece_01.png` à `piece_04.png`) et génère `positions_carte.rpy`, utilisé par l'écran de reconstitution de la carte.
2. **`outils/nettoyer_assets.py`** — les générateurs d'images IA simulent souvent la transparence par un damier gris/blanc au lieu d'un vrai canal alpha, et regroupent parfois plusieurs états d'un bouton (normal/survolé) sur une seule image. Ce script détecte et retire le damier, recadre l'élément utile, et sépare les visuels assemblés. Les originaux sont sauvegardés avant modification.

Les images livrées avec le jeu sont en JPEG ou WebP compressé (environ 6 Mo au total). Les `.png` de `game/images/` (environ 65 Mo de sources IA et de doublons) sont **exclus du build** par `options.rpy` : ils ne partent ni dans les exports ni dans la démo web. Les originaux peuvent aussi être rangés dans `assets_sources/` (non versionné) ; `ranger_images.bat` les y déplace.

```bash
pip install pillow
python decoupage_carte.py
python outils/nettoyer_assets.py game/images/ui/cursor.png game/images/ui/icone.webp 96     # damier clair ou fond blanc
python outils/nettoyer_assets.py --sombre SOURCE.png SORTIE.webp 96                            # damier noir/gris
python outils/nettoyer_assets.py --fond SOURCE.png game/images/backgrounds/bg_x.jpg            # décor entouré de damier
```

## État actuel et limitations connues

- **Interface dessinée** : le jeu utilise des boutons et cadres unis générés par Ren'Py plutôt que les PNG de `images/ui/`. Ces PNG contiennent encore un faux damier et ne sont pas livrés dans le build : aucun écran ne doit y faire référence (Ren'Py précharge les images de toutes les branches d'un écran, et la démo web plante sur un fichier absent). Pour les utiliser, les nettoyer (`outils/nettoyer_assets.py`), les enregistrer en `.webp`, puis adapter `gm_panel` et `gm_bouton` dans `screens.rpy`.
- **Carte en anglais** : le plan (« Manor of Blackwood ») est en anglais. C'est assumé dans l'histoire : il a été relevé par Edmund Blackwood, un cartographe anglais. Pour une carte en français, il faudrait régénérer `map_full.png` puis relancer `decoupage_carte.py`.
- **Audio** : ambiances et bruitages sont fabriqués par synthèse (`python synthese_sons.py`, nécessite numpy et ffmpeg), donc libres de droits. Ils peuvent être remplacés par des enregistrements en gardant les mêmes noms de fichiers dans `game/audio/`.
- **Mode développeur** : `config.developer = "auto"` ; la console n'est disponible que depuis le SDK, jamais dans les builds ni la démo web.

## Roadmap

- [x] Câbler les icônes (clé, fragment) et le curseur personnalisé
- [x] Mettre à jour `config.name` dans `options.rpy`
- [x] Intégrer musique d'ambiance et bruitages (portes, bonne/mauvaise réponse)
- [x] Pouvoirs des fragments, double mise, porte de sortie, 4 fins
- [x] Historique des dialogues et menu rapide
- [ ] Utiliser les boutons et cadres illustrés une fois les PNG nettoyés (en .webp)
- [ ] Finaliser l'ensemble des illustrations (fonds de porte, carte en français)

## Outils et crédits

- Moteur de jeu : [Ren'Py](https://www.renpy.org/) (Python)
- Traitement d'images : [Pillow](https://python-pillow.org/)
- Polices : [Crimson Text](https://fonts.google.com/specimen/Crimson+Text) et [IM Fell English SC](https://fonts.google.com/specimen/IM+Fell+English+SC), sous licence SIL Open Font License (voir `game/fonts/`)
- Direction artistique : génération d'images IA (prompts sur mesure, cf. documentation de production), retravaillées via scripts maison
- Développement : Diaby Mamadou Dian
