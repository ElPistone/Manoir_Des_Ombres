########################################
# LE MANOIR-LABYRINTHE — ui_style.rpy
# Couleurs, mode d'interface et mise à l'échelle des fonds
########################################

## Palette --------------------------------------------------------
define gm_gold = "#c9a24a"
define gm_gold_light = "#f4e4bc"
define gm_bordeaux = "#3b1524"
define gm_night = "#0d1524ee"
define gm_parchemin = "#e8dcc0"

## Mode d'interface -----------------------------------------------
# False = boutons et cadres dessinés par Ren'Py (toujours propres)
# True  = utilise les PNG de images/ui/ (à activer APRES les avoir
#         nettoyés avec nettoyer_assets.py)
define gm_art_ui = False

## Valeurs par défaut de la carte ---------------------------------
# positions_carte.rpy (généré par decoupage_carte.py) écrasera ces valeurs.
init -1 python:
    map_pieces_positions = {}
    map_full_width = 1000
    map_full_height = 500

## Fonds redimensionnés à la taille de l'écran --------------------
# Tous les fichiers "bg_*" du dossier images/ sont enregistrés avec
# le même nom qu'avant (ex: "bg_manor_facade"), mais mis à l'échelle
# de l'écran en mode "cover" (remplit tout l'écran sans déformer).
init 10 python:
    for _f in renpy.list_files():
        _nom = _f.split("/")[-1]
        if _f.startswith("images/") and _nom.startswith("bg_") and _nom.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            _id = _nom.rsplit(".", 1)[0]
            renpy.image(_id, Transform(_f, xysize=(config.screen_width, config.screen_height), fit="cover", align=(0.5, 0.5)))
