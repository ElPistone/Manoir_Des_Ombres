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

# Icône de la fenêtre : prévoir un fichier dédié 256x256 (window_icon.png)
# recommandé plutôt que de réutiliser icon_score.png en production.
define config.window_icon = "images/ui/icon_score.png"


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

# On empêche le Ctrl-skip et le clic rapide de "sauter" une énigme
# sans que le joueur ait réellement répondu : les écrans choix_piece et
# menu_enigme sont "modal", donc déjà protégés, mais on verrouille aussi
# le skip global pour rester cohérent avec la tension du jeu.
define config.allow_skipping = True

# Vitesse de défilement du texte par défaut (caractères/seconde)
default preferences.text_cps = 40


## Rollback (retour en arrière) ------------------------------------

# On désactive le rollback pendant les énigmes serait idéal (pour empêcher
# un joueur de "annuler" une mauvaise réponse) : cela se gère avec
# $ renpy.block_rollback() juste après chaque tirage de résultat dans
# script.rpy plutôt qu'ici, mais on limite déjà la profondeur globale :
define config.rollback_enabled = True
define config.rollback_length = 20


## Musique / son ------------------------------------------------

# define config.main_menu_music = "audio/music/ambiance.ogg"


## Divers ------------------------------------------------------

define config.developer = True  # passer à False avant la diffusion finale
