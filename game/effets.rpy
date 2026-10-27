########################################
# LE MANOIR-LABYRINTHE — effets.rpy
# Transitions et animations (ATL) de l'interface
########################################

## Transitions de scène --------------------------------------------
define fondu_lent = Dissolve(1.2)
define fondu_noir = Fade(0.6, 0.2, 0.6)
define eclat_or = Fade(0.08, 0.0, 0.6, color="#c9a24a")
define eclat_rouge = Fade(0.08, 0.1, 0.8, color="#5a0f1c")
define fin_partie = Fade(1.0, 0.6, 1.8)

# La boîte de dialogue gère sa propre animation (parchemin_deroule)
define config.window_show_transition = None
define config.window_hide_transition = None


## Boîte de dialogue ---------------------------------------------------

# Le parchemin se déroule depuis le centre quand la boîte apparaît,
# et s'enroule quand elle disparaît (changement de scène, énigme...)
transform parchemin_deroule:
    crop_relative True
    on show:
        crop (0.49, 0.0, 0.02, 1.0)
        alpha 0.0
        easein 0.5 crop (0.0, 0.0, 1.0, 1.0) alpha 1.0
    on hide:
        easeout 0.3 crop (0.49, 0.0, 0.02, 1.0) alpha 0.0

# Indicateur « cliquer pour continuer » qui pulse en fin de texte
transform clignote:
    alpha 1.0
    easeout 0.6 alpha 0.25
    easein 0.6 alpha 1.0
    repeat


## Écrans modaux -------------------------------------------------------

transform voile_apparait:
    on show:
        alpha 0.0
        linear 0.3 alpha 1.0
    on hide:
        linear 0.25 alpha 0.0

transform panneau_apparait:
    on show:
        alpha 0.0
        yoffset 40
        easein 0.4 alpha 1.0 yoffset 0
    on hide:
        easeout 0.2 alpha 0.0 yoffset 20

# Apparition décalée des boutons (d = délai en secondes)
transform bouton_apparait(d=0.0):
    alpha 0.0
    yoffset 15
    pause d
    easein 0.3 alpha 1.0 yoffset 0

# Le bouton s'éclaire au survol, sans changer de taille
transform bouton_survol:
    on idle:
        easein 0.15 matrixcolor BrightnessMatrix(0.0)
    on hover:
        easein 0.15 matrixcolor BrightnessMatrix(0.12)


## Mise d'un fragment ---------------------------------------------------

# Le fragment misé apparaît puis glisse sous la porte
transform fragment_glisse:
    subpixel True
    xalign 0.5
    yalign 0.4
    zoom 0.5
    rotate -4
    alpha 0.0
    easein 0.4 alpha 1.0
    pause 0.5
    easein 0.9 yalign 1.3 zoom 0.3 rotate 8 alpha 0.0


## Notifications ---------------------------------------------------------

transform notif_apparait:
    on show:
        alpha 0.0
        yoffset -30
        easein 0.35 alpha 1.0 yoffset 0
    on hide:
        linear 0.5 alpha 0.0
