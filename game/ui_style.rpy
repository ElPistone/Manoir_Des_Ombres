########################################
# LE MANOIR DES OMBRES — ui_style.rpy
# Couleurs, mode d'interface et mise à l'échelle des fonds
########################################

## Palette --------------------------------------------------------
define gm_gold = "#c9a24a"
define gm_gold_light = "#f4e4bc"
define gm_bordeaux = "#3b1524"
define gm_night = "#0d1524ee"
define gm_parchemin = "#e8dcc0"
define gm_parchemin_sombre = "#b8a988"
define gm_encre = "#2b1d0e"

## Polices (libres, licence OFL : voir fonts/OFL-*.txt) ---------------
# Crimson Text pour la lecture, IM Fell English SC pour les titres et boutons
define gm_police_titre = "fonts/IMFellEnglishSC.ttf"

style default:
    font "fonts/CrimsonText-Regular.ttf"

# {b} et {i} utilisent les vraies variantes de la police, pas un faux gras
init python:
    config.font_replacement_map["fonts/CrimsonText-Regular.ttf", True, False] = ("fonts/CrimsonText-SemiBold.ttf", False, False)
    config.font_replacement_map["fonts/CrimsonText-Regular.ttf", False, True] = ("fonts/CrimsonText-Italic.ttf", False, False)

style gm_titre is default:
    font "fonts/IMFellEnglishSC.ttf"
    color "#e8dcc0"

## Interface ---------------------------------------------------------
# Boutons et cadres sont dessinés par Ren'Py (screens.rpy). Les PNG bruts de
# images/ui/ (boutons, cadres) contiennent un faux damier et ne sont pas
# livrés dans le build. Pour les utiliser un jour : les nettoyer avec
# outils/nettoyer_assets.py, les enregistrer en .webp, puis modifier
# gm_panel et gm_bouton dans screens.rpy.

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
# Si un même fond existe en .png et en .jpg, la version .jpg (légère) l'emporte.
init 10 python:
    for _f in sorted(renpy.list_files(), key=lambda f: not f.lower().endswith(".png")):
        _nom = _f.split("/")[-1]
        if _f.startswith("images/") and _nom.startswith("bg_") and _nom.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            _id = _nom.rsplit(".", 1)[0]
            renpy.image(_id, Transform(_f, xysize=(config.screen_width, config.screen_height), fit="cover", align=(0.5, 0.5)))
