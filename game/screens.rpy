########################################
# LE MANOIR-LABYRINTHE — screens.rpy
# Écrans du jeu : composants, gameplay, menu principal, sauvegarde
########################################

## ------------------------------------------------------------
## COMPOSANTS RÉUTILISABLES
## ------------------------------------------------------------

# Panneau : cadre doré + fond nuit (ou PNG si gm_art_ui = True)
screen gm_panel(pad=40, xa=0.5, ya=0.5):
    if gm_art_ui:
        frame:
            align (xa, ya)
            background Frame("images/ui/frame_ui_generic.png", 80, 80)
            padding (pad, pad)
            transclude
    else:
        frame:
            align (xa, ya)
            background Solid(gm_gold)
            padding (3, 3)
            frame:
                background Solid(gm_night)
                padding (pad, pad)
                transclude


# Bouton : label, action, largeur, hauteur, taille du texte, image (mode PNG)
screen gm_bouton(label, act, w=420, h=80, fs=28, img="btn_start"):
    button:
        xsize w
        ysize h
        action act
        padding (3, 3)
        background (Frame("images/ui/" + img + ".png", 40, 40) if gm_art_ui else Solid(gm_gold))
        hover_background (Frame("images/ui/" + img + "_hover.png", 40, 40) if gm_art_ui else Solid(gm_gold_light))
        if gm_art_ui:
            text label size fs color gm_parchemin hover_color gm_gold_light xalign 0.5 yalign 0.5
        else:
            frame:
                background Solid(gm_bordeaux)
                xfill True
                yfill True
                padding (0, 0)
                text label size fs color gm_parchemin hover_color gm_gold_light xalign 0.5 yalign 0.5 text_align 0.5


## ------------------------------------------------------------
## BOÎTE DE DIALOGUE (remplace le "say" par défaut de Ren'Py)
## ------------------------------------------------------------

screen say(who, what):
    style_prefix "say"
    zorder 50

    window:
        id "window"
        xalign 0.5
        yalign 1.0
        xsize 1400
        ysize 400
        yoffset -30
        padding (63, 73)
        background Transform(
            Frame("images/ui/frame_dialogue.jpg", 220, 140, 220, 160),
            xysize=(1400, 400)
        )

        vbox:
            xfill True
            yalign 0.5
            spacing 10

            if who is not None:
                text who id "who" color gm_bordeaux size 24 bold True

            text what id "what" color "#2b1d0e" size 28 line_spacing 8 xfill True


## ------------------------------------------------------------
## ÉCRANS DE GAMEPLAY
## ------------------------------------------------------------

# --- Choix du morceau de carte à miser ---
screen choix_piece(pieces):
    modal True
    zorder 200

    add Solid("#000000aa")

    use gm_panel(pad=50):
        vbox:
            spacing 30

            text "Quel morceau de carte allez-vous miser ?" size 32 color gm_parchemin xalign 0.5

            hbox:
                xalign 0.5
                xsize 690
                spacing 15
                box_wrap True
                box_wrap_spacing 15

                for piece in pieces:
                    button:
                        xysize (120, 120)
                        action Return(piece)
                        padding (3, 3)
                        background Solid(gm_gold)
                        hover_background Solid(gm_gold_light)
                        frame:
                            background Solid(gm_bordeaux)
                            xfill True
                            yfill True
                            padding (0, 0)
                            text piece.replace("piece_", "N° ") size 26 color gm_parchemin hover_color gm_gold_light xalign 0.5 yalign 0.5


# --- Énigme à choix multiples : 2 réponses par ligne, sur 2 lignes ---
# Renvoie le texte de la réponse choisie (les réponses sont mélangées).
screen menu_enigme(riddle_text, choices):
    modal True
    zorder 200

    add Solid("#000000aa")

    use gm_panel(pad=50):
        vbox:
            spacing 40

            text riddle_text color gm_parchemin size 32 xsize 1000 text_align 0.5 xalign 0.5

            hbox:
                xalign 0.5
                xsize 1020
                spacing 30
                box_wrap True
                box_wrap_spacing 30

                for option in choices:
                    use gm_bouton(option, Return(option), 490, 90, 26, "frame_dialogue")


# --- HUD (haut droite) : porte en cours, score + accès à la carte ---
screen hud_jeu():
    zorder 100

    hbox:
        xalign 0.98
        yalign 0.03
        spacing 15

        frame:
            background Solid("#0d1524cc")
            padding (18, 8)
            text ("Porte : %d/%d" % (min(niveau + 1, serie_requise), serie_requise)) size 26 color gm_gold

        frame:
            background Solid("#0d1524cc")
            padding (18, 8)
            text ("Score : %d" % score) size 26 color gm_gold

        button:
            background Solid("#0d1524cc")
            hover_background Solid(gm_bordeaux)
            padding (18, 8)
            action Show("carte_puzzle")
            text ("Carte : %d/%d" % (len(pieces_owned), total_pieces)) size 26 color gm_gold hover_color gm_gold_light


# --- Carte en cours de reconstitution ---
screen carte_puzzle():
    modal True
    zorder 250

    add Solid("#000000bb")

    use gm_panel(pad=40):
        vbox:
            spacing 25

            text "Votre carte" size 34 color gm_parchemin xalign 0.5

            if map_pieces_positions:
                # Vraie carte (nécessite positions_carte.rpy et images/map/piece_XX.png)
                $ echelle = min(900.0 / map_full_width, 640.0 / map_full_height)
                fixed:
                    xalign 0.5
                    xysize (int(map_full_width * echelle), int(map_full_height * echelle))
                    add Solid("#1a2236")
                    for pid in pieces_owned:
                        if pid in map_pieces_positions and renpy.loadable("images/map/" + pid + ".png"):
                            $ pp = map_pieces_positions[pid]
                            add Transform("images/map/" + pid + ".png", xysize=(int(pp["width"] * echelle), int(pp["height"] * echelle))) xpos int(pp["x"] * echelle) ypos int(pp["y"] * echelle)
            else:
                # Version simplifiée : une tuile par morceau
                hbox:
                    xalign 0.5
                    xsize 820
                    spacing 12
                    box_wrap True
                    box_wrap_spacing 12

                    for n in range(1, total_pieces + 1):
                        $ pid = "piece_%02d" % n
                        frame:
                            xysize (150, 90)
                            background (Solid(gm_gold) if pid in pieces_owned else Solid("#1a2236"))
                            text ("N° %d" % n) xalign 0.5 yalign 0.5 size 24 color (gm_bordeaux if pid in pieces_owned else "#5b6478")

            textbutton "Fermer" action Hide("carte_puzzle") xalign 0.5 text_color gm_gold text_hover_color gm_gold_light text_size 26


## ------------------------------------------------------------
## ÉCRAN TITRE
## ------------------------------------------------------------

screen main_menu():
    tag menu

    add "bg_title"

    add Transform("images/ui/logo_title.png", xysize=(760, 520), fit="contain") xalign 0.5 ypos 30

    vbox:
        xalign 0.5
        ypos 640
        spacing 20

        use gm_bouton("Commencer", Start(), 420, 80, 30, "btn_start")
        use gm_bouton("Charger", ShowMenu("load"), 420, 80, 30, "btn_load")
        use gm_bouton("Quitter", Quit(confirm=True), 420, 80, 30, "btn_quit")


## ------------------------------------------------------------
## MENU DE JEU (conteneur Sauvegarder / Charger)
## ------------------------------------------------------------

screen game_menu(title, scroll=None):
    tag menu

    if renpy.has_image("bg_entrance_hall"):
        add "bg_entrance_hall"
    else:
        add Solid("#000000")
    add Solid("#000000aa")

    frame:
        align (0.5, 0.42)
        background Solid(gm_gold)
        padding (3, 3)
        frame:
            background Solid(gm_night)
            padding (40, 30)
            vbox:
                spacing 20
                text title color gm_parchemin size 34 xalign 0.5
                transclude

    use navigation


screen navigation():
    hbox:
        align (0.5, 0.95)
        spacing 40

        textbutton "Retour" action Return() text_color gm_gold text_hover_color gm_gold_light text_size 26
        textbutton "Sauvegarder" action ShowMenu("save") text_color gm_gold text_hover_color gm_gold_light text_size 26
        textbutton "Charger" action ShowMenu("load") text_color gm_gold text_hover_color gm_gold_light text_size 26
        textbutton "Menu principal" action MainMenu(confirm=True) text_color gm_gold text_hover_color gm_gold_light text_size 26


## ------------------------------------------------------------
## SAUVEGARDE / CHARGEMENT (12 emplacements)
## ------------------------------------------------------------

screen save():
    use game_menu(_("Sauvegarder votre partie")):
        use file_slots


screen load():
    use game_menu(_("Charger une partie")):
        use file_slots


screen file_slots():
    grid 3 4:
        xalign 0.5
        spacing 20

        for i in range(1, 13):
            button:
                xysize (420, 130)
                action FileAction(i)
                padding (3, 3)
                background Solid(gm_gold)
                hover_background Solid(gm_gold_light)

                frame:
                    background Solid(gm_bordeaux)
                    xfill True
                    yfill True
                    padding (10, 10)

                    hbox:
                        spacing 15
                        yalign 0.5

                        add FileScreenshot(i) xysize (160, 90) fit "contain"

                        vbox:
                            yalign 0.5
                            text FileSlotName(i) color gm_gold size 20
                            text FileTime(i, format=_("%d/%m/%Y - %H:%M"), empty=_("Emplacement vide")) color gm_parchemin size 16


## ------------------------------------------------------------
## CONFIRMATION (Quitter, Menu principal...)
## ------------------------------------------------------------

screen confirm(message, yes_action, no_action):
    modal True
    zorder 300

    add Solid("#000000cc")

    use gm_panel(pad=40):
        vbox:
            spacing 30

            text message color gm_parchemin size 28 xsize 700 text_align 0.5 xalign 0.5

            hbox:
                xalign 0.5
                spacing 30
                use gm_bouton("Oui", yes_action, 200, 70, 26, "btn_start")
                use gm_bouton("Non", no_action, 200, 70, 26, "btn_quit")
