########################################
# LE MANOIR DES OMBRES — options.rpy
# Configuration générale du jeu
########################################

## Identité du jeu -------------------------------------------

define config.name = _("Le Manoir des Ombres")
define config.version = "1.1"
define build.name = "LeManoirLabyrinthe"

# Titre de la fenêtre (identique au nom du jeu)
define config.window_title = config.name

# Icône de la fenêtre (256x256). Rangée dans gui/ car les .png de images/
# ne sont pas livrés dans le build (voir plus bas).
define config.window_icon = "gui/window_icon.png"

# Curseur personnalisé : une petite clé ancienne (pointe en haut à gauche)
define config.mouse = {"default": [("gui/curseur_cle.png", 2, 2)]}


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

# Dossier de sauvegarde unique au jeu (nom conservé tel quel pour ne pas
# perdre les sauvegardes existantes) (évite tout conflit avec un autre
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
# Contre la triche par sauvegarde : le menu est bloqué pendant la mise et
# l'énigme, et le manoir mémorise chaque verdict (persistent.verdicts) :
# recharger une partie devant une porte déjà répondue rejoue le même verdict.
define config.rollback_enabled = False
define config.hard_rollback_limit = 0


## Musique / son ------------------------------------------------

# Tous les sons sont fabriqués par synthese_sons.py (aucun droit d'auteur)
define config.main_menu_music = "audio/ambiance_manoir.ogg"
define config.fadeout_audio = 1.5


## Build ------------------------------------------------------

# Les originaux lourds (PNG non compressés) ne sont jamais livrés avec le jeu.
# Le jeu n'utilise que des .jpg / .webp dans images/ : les ~65 Mo de .png
# (sources IA, doublons, éléments non utilisés) restent dans le dépôt pour
# le travail, mais ne partent plus dans le build (ni dans la démo web).
init python:
    build.classify("assets_sources/**", None)
    build.classify("outils/**", None)
    build.classify("game/images/**.png", None)
    build.classify("**.bat", None)
    build.classify("**.py", None)


## Divers ------------------------------------------------------

# "auto" : mode développeur (console, rechargement Maj+R) actif quand on lance
# le jeu depuis le SDK, mais désactivé dans les builds distribués et la démo
# web (sinon n'importe qui pourrait ouvrir la console et tricher).
define config.developer = "auto"
