########################################
# LE MANOIR-LABYRINTHE — options.rpy
# Configuration générale du jeu
########################################

## Identité du jeu -------------------------------------------

define config.name = _("Le Manoir-Labyrinthe")
define config.version = "1.0"
define build.name = "LeManoirLabyrinthe"

# Titre de la fenêtre (identique au nom du jeu)
define config.window_title = config.name

# Icône de la fenêtre (256x256, tirée de icon_score.png)
define config.window_icon = "images/ui/icon_window.png"


## Résolution & affichage -------------------------------------

# (résolution gérée par gui.init dans gui.rpy)

# Pas de nom de personnage par défaut affiché (le narrateur est "None")
define config.window = "auto"


## Transitions --------------------------------------------------

define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.end_game_transition = dissolve


## Sauvegarde -----------------------------------------------------

# Dossier de sauvegarde unique au jeu (évite tout conflit avec un autre
# jeu Ren'Py installé sur la même machine).
define config.save_directory = "LeManoirLabyrinthe-1745201"

define config.has_autosave = True
define config.autosave_on_quit = True
define config.autosave_frequency = 3  # minutes


## Confort de lecture / anti-triche des énigmes -------------------

# Le skip n'avance que dans le texte déjà lu : les écrans choix_piece et
# menu_enigme sont "modal" et attendent toujours une vraie réponse.
define config.allow_skipping = True

# Vitesse de défilement du texte par défaut (caractères/seconde)
default preferences.text_cps = 40


## Rollback (retour en arrière) ------------------------------------

# Désactivé : une réponse est définitive, le joueur ne peut pas revenir
# en arrière pour corriger une erreur. script.rpy appelle aussi
# renpy.block_rollback() après chaque réponse, par sécurité.
define config.rollback_enabled = False
define config.hard_rollback_limit = 0


## Musique / son ------------------------------------------------

# Tous les sons sont fabriqués par synthese_sons.py (aucun droit d'auteur)
define config.main_menu_music = "audio/ambiance_manoir.ogg"
define config.fadeout_audio = 1.5


## Build ------------------------------------------------------

# Les originaux lourds (PNG non compressés) ne sont jamais livrés avec le jeu.
init python:
    build.classify("assets_sources/**", None)
    build.classify("**.bat", None)
    build.classify("**.py", None)


## Divers ------------------------------------------------------

define config.developer = True  # passer à False avant la diffusion finale
