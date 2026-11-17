########################################
# LE MANOIR DES OMBRES — screens.rpy
# Écrans du jeu : composants, gameplay, menu principal, sauvegarde
########################################

## ------------------------------------------------------------
## COMPOSANTS RÉUTILISABLES
## ------------------------------------------------------------

# Panneau : cadre doré + fond nuit.
# (Les PNG de cadres et de boutons de images/ui/ ne sont pas livrés dans le
# build : aucun écran ne doit y faire référence, même dans une branche « if »
# inactive, car Ren'Py précharge aussi ces images et la version web plante.)
screen gm_panel(pad=40, xa=0.5, ya=0.5):
    frame:
        at panneau_apparait
        align (xa, ya)
        background Solid(gm_gold)
        padding (3, 3)
        frame:
            background Solid(gm_night)
            padding (pad, pad)
            transclude


# Bouton : label, action, largeur, hauteur, taille du texte, image (ignorée,
# gardée pour compatibilité), délai d'apparition (pour faire entrer les
# boutons l'un après l'autre). Avec act=None, le bouton est inactif et grisé.
screen gm_bouton(label, act, w=420, h=80, fs=28, img="btn_start", d=0.0):
    frame:
        at bouton_apparait(d)
        background None
        padding (0, 0)
        button:
            at bouton_survol
            xsize w
            ysize h
            action act
            activate_sound "audio/clic.ogg"
            padding (3, 3)
            background Solid(gm_gold if act is not None else "#6b5a35")
            hover_background Solid(gm_gold_light)
            frame:
                background Solid(gm_bordeaux if act is not None else "#24141b")
                xfill True
                yfill True
                padding (8, 0)
                text label style "gm_titre" size fs color (gm_parchemin if act is not None else "#7d7262") hover_color gm_gold_light xalign 0.5 yalign 0.5 text_align 0.5


## ------------------------------------------------------------
## BOÎTE DE DIALOGUE (remplace le "say" par défaut de Ren'Py)
## ------------------------------------------------------------

screen say(who, what):
    style_prefix "say"
    zorder 50

    window:
        id "window"
        at parchemin_deroule
        xalign 0.5
        yalign 1.0
        # Cadre taillé sur mesure (fabriquer_cadre_dialogue.py) : 3 lignes
        # de texte au maximum, ornements jamais déformés.
        xsize 1240
        ysize (270 if persistent.texte_grand else 230)
        yoffset -24
        padding (100, 34, 100, 34)
        background "images/ui/frame_dialogue_bas.jpg"

        vbox:
            xfill True
            yalign 0.5
            spacing 6

            if who is not None:
                text who id "who" color gm_bordeaux size 26 bold True

            # Encre brune sur parchemin : bien lisible
            text what id "what" color gm_encre size tx(30) line_spacing 4 xfill True


## ------------------------------------------------------------
## MENU RAPIDE (en bas à droite, à côté de la boîte de dialogue)
## ------------------------------------------------------------

default quick_menu = True

init python:
    config.overlay_screens.append("quick_menu")

style gm_quick_button is default:
    xalign 1.0
    padding (10, 3)
style gm_quick_button_text is gm_titre:
    size 22
    color "#c9a24aaa"
    hover_color "#f4e4bc"
    insensitive_color "#c9a24a44"

screen quick_menu():
    zorder 100

    if quick_menu:
        vbox:
            style_prefix "gm_quick"
            xalign 0.995
            yalign 0.975
            spacing 0

            textbutton "Historique" action ShowMenu("history")
            textbutton "Sauvegarder" action ShowMenu("save")
            textbutton "Charger" action ShowMenu("load")
            textbutton "Réglages" action ShowMenu("preferences")
            textbutton "Menu" action MainMenu()


## ------------------------------------------------------------
## ÉCRANS DE GAMEPLAY
## ------------------------------------------------------------

# --- Choix du ou des morceaux de carte à miser ---
# Renvoie toujours une liste : [piece] ou, en double mise, [piece_a, piece_b].
screen choix_piece(pieces, double_possible=False, sortie=False):
    modal True
    zorder 200

    default mode_double = False
    default selection = []

    add Solid("#000000aa") at voile_apparait

    use gm_panel(pad=45):
        vbox:
            spacing 22
            xsize 1160

            if sortie:
                text "Quel morceau risquez-vous à la porte de sortie ?" style "gm_titre" size 38 xalign 0.5
            elif mode_double:
                text "Choisissez les deux morceaux à miser" style "gm_titre" size 38 xalign 0.5
            else:
                text "Quel morceau de carte allez-vous miser ?" style "gm_titre" size 38 xalign 0.5

            text "Le morceau misé reste sous la porte : son pouvoir ne vous aidera pas pour cette énigme." size 25 color gm_parchemin_sombre xalign 0.5 text_align 0.5

            hbox:
                xalign 0.5
                spacing 20

                for i, piece in enumerate(pieces):
                    $ frag = fragments[piece]
                    $ choisi = piece in selection
                    frame:
                        at bouton_apparait(0.1 + i * 0.08)
                        background None
                        padding (0, 0)
                        button:
                            at bouton_survol
                            xysize (260, 340)
                            padding (3, 3)
                            background Solid(gm_gold_light if choisi else gm_gold)
                            hover_background Solid(gm_gold_light)
                            activate_sound "audio/clic.ogg"
                            action (ToggleSetMembership(selection, piece) if mode_double else Return([piece]))

                            frame:
                                background Solid("#2a1019" if choisi else "#140d16")
                                xfill True
                                yfill True
                                padding (10, 10)
                                vbox:
                                    spacing 8
                                    xfill True
                                    add Transform("images/map/" + piece + ".jpg", xysize=(234, 150), fit="cover") xalign 0.5
                                    text frag["nom"] style "gm_titre" size 23 color gm_gold xalign 0.5 text_align 0.5
                                    if piece == "piece_04" and cle_utilisee:
                                        text "Pouvoir déjà utilisé." size 21 color "#8a7f6a" xalign 0.5 text_align 0.5
                                    else:
                                        text frag["effet"] size 21 color gm_parchemin xalign 0.5 text_align 0.5

            if double_possible:
                vbox:
                    spacing 12
                    xalign 0.5
                    hbox:
                        xalign 0.5
                        spacing 30
                        if mode_double:
                            use gm_bouton("Valider la double mise", (Return(list(selection)) if len(selection) == 2 else None), 460, 70, 27, d=0.0)
                            use gm_bouton("Annuler", [SetScreenVariable("mode_double", False), SetScreenVariable("selection", [])], 240, 70, 27, d=0.0)
                        else:
                            use gm_bouton("Tout risquer : miser les deux", SetScreenVariable("mode_double", True), 520, 70, 27, d=0.4)
                    text "Double mise : énigme plus difficile, mais deux morceaux gagnés si vous répondez juste. Une erreur vous coûte les deux." size 22 color gm_parchemin_sombre xalign 0.5 text_align 0.5 xsize 1000


# --- Énigme : à choix multiples (2 réponses par ligne) ou à réponse libre ---
# Renvoie le texte de la réponse, ou "__sablier__" pour changer d'énigme.
screen menu_enigme(enigme, choix, actifs=[], barree=None, sablier_dispo=False, indice_dispo=False, implorer_dispo=False):
    modal True
    zorder 200

    default reponse = ""

    add Solid("#000000aa") at voile_apparait

    use gm_panel(pad=45):
        hbox:
            spacing 40

            if enigme.get("illus"):
                add Transform("images/riddles/enigme_" + enigme["illus"] + ".webp", xysize=(340, 340), fit="contain") yalign 0.5 at voile_apparait

            vbox:
                spacing 28
                xsize (960 if enigme.get("illus") else 1080)

                text enigme["riddle"] color gm_parchemin size tx(36) xalign 0.5 text_align 0.5 xfill True

                # Pouvoir de la Lanterne (ou indice imploré) : un indice
                if indice_dispo:
                    text ("{i}" + ("Lanterne : " if "Lanterne" in actifs else "La voix : ") + enigme["indice"] + "{/i}") size tx(26) color gm_gold_light xalign 0.5 text_align 0.5 xfill True

                if enigme.get("saisie"):
                    # Pouvoir de l'Encre : la première lettre
                    if "Encre" in actifs:
                        text ("{i}Encre : la réponse commence par « " + premiere_lettre(enigme) + " ».{/i}") size tx(26) color gm_gold_light xalign 0.5 text_align 0.5

                    frame:
                        xalign 0.5
                        xsize 700
                        background Solid(gm_gold)
                        padding (3, 3)
                        frame:
                            background Solid(gm_bordeaux)
                            xfill True
                            padding (20, 12)
                            input:
                                value ScreenVariableInputValue("reponse", returnable=True)
                                length 32
                                pixel_width 640
                                size 34
                                color gm_parchemin
                                xalign 0.5

                    text "Tapez votre réponse puis appuyez sur Entrée." size 22 color gm_parchemin_sombre xalign 0.5
                    hbox:
                        xalign 0.5
                        use gm_bouton("Répondre", (Return(reponse) if reponse.strip() else None), 320, 70, 28, d=0.3)

                else:
                    hbox:
                        xalign 0.5
                        spacing 30
                        box_wrap True
                        box_wrap_spacing 30
                        xsize (940 if enigme.get("illus") else 1020)

                        for i, option in enumerate(choix):
                            # Pouvoir de l'Encre : une mauvaise réponse barrée
                            if option == barree:
                                use gm_bouton("{s}" + option + "{/s}", None, (455 if enigme.get("illus") else 490), 90, tx(27), "frame_dialogue", d=0.25 + i * 0.1)
                            else:
                                use gm_bouton(option, Return(option), (455 if enigme.get("illus") else 490), 90, tx(27), "frame_dialogue", d=0.25 + i * 0.1)

                use actions_enigme(sablier_dispo, implorer_dispo)


# Sablier (autre énigme) et indice imploré (la bougie raccourcit)
screen actions_enigme(sablier_dispo, implorer_dispo):
    if sablier_dispo or implorer_dispo:
        hbox:
            xalign 0.5
            spacing 50
            # Pouvoir du Sablier : une autre énigme, une fois par porte
            if sablier_dispo:
                textbutton "Retourner le sablier (autre énigme)":
                    action Return("__sablier__")
                    text_style "gm_titre"
                    text_size tx(25)
                    text_color gm_gold
                    text_hover_color gm_gold_light
            # Sans la Lanterne, on peut implorer un indice contre une porte de bougie
            if implorer_dispo:
                textbutton "Implorer un indice (la bougie raccourcit)":
                    action Return("__implorer__")
                    text_style "gm_titre"
                    text_size tx(25)
                    text_color gm_gold
                    text_hover_color gm_gold_light


# --- Choix de la porte : chêne (énigme à choix) ou murmure (fouille / saisie) ---
define portes_au_choix = [
    (False, "La porte de chêne", "Une énigme, et quelques réponses gravées dans le bois. Il suffit de choisir la bonne."),
    (True, "La porte qui murmure", "Aucune réponse proposée : fouillez la pièce, ou trouvez le mot seul. Si vous répondez juste, la bougie gagne une porte et une page du journal vous attend."),
]

# Renvoie True pour la porte qui murmure.
screen choix_porte(salle, restantes):
    modal True
    zorder 200

    add Solid("#000000aa") at voile_apparait

    use gm_panel(pad=45):
        vbox:
            spacing 26
            xsize 1160

            text "Deux portes se font face. Laquelle ouvrez-vous ?" style "gm_titre" size tx(38) xalign 0.5 text_align 0.5

            hbox:
                xalign 0.5
                spacing 40

                for i, option in enumerate(portes_au_choix):
                    $ murmure, titre, texte = option
                    frame:
                        at bouton_apparait(0.1 + i * 0.12)
                        background None
                        padding (0, 0)
                        button:
                            at bouton_survol
                            xysize (520, 300)
                            padding (3, 3)
                            background Solid(gm_gold)
                            hover_background Solid(gm_gold_light)
                            activate_sound "audio/porte_grince.ogg"
                            action Return(murmure)
                            frame:
                                background Solid("#2a1019" if murmure else "#140d16")
                                xfill True
                                yfill True
                                padding (24, 20)
                                vbox:
                                    spacing 14
                                    xfill True
                                    text titre style "gm_titre" size tx(32) color gm_gold xalign 0.5
                                    text texte size tx(23) color gm_parchemin xalign 0.5 text_align 0.5

            $ texte_bougie = ("Votre bougie peut encore éclairer %d porte%s après celle-ci." % (restantes, "s" if restantes > 1 else "")) if restantes > 0 else "Votre bougie vit sa dernière porte."
            text texte_bougie size tx(23) color gm_parchemin_sombre xalign 0.5


# --- Fouille : on clique sur l'objet décrit, dans la pièce elle-même ---
# Renvoie le nom de la zone choisie, "__sablier__" ou "__implorer__".
screen fouille_salle(enigme, barree=None, indice_dispo=False, sablier_dispo=False, implorer_dispo=False):
    modal True
    zorder 200

    # Les zones cliquables, éclairées au survol
    for nom, zone in sorted(enigme["zones"].items()):
        $ x0, y0, x1, y1 = zone
        $ zx, zy = int(x0 * config.screen_width), int(y0 * config.screen_height)
        $ zw, zh = int((x1 - x0) * config.screen_width), int((y1 - y0) * config.screen_height)
        if nom == barree:
            # Pouvoir de l'Encre : une mauvaise piste est barrée
            frame:
                pos (zx, zy)
                xysize (zw, zh)
                background Solid("#5a0f1c55")
                text "✕" font "DejaVuSans.ttf" size 60 color "#c9a24acc" align (0.5, 0.5)
        else:
            button:
                pos (zx, zy)
                xysize (zw, zh)
                padding (0, 0)
                background None
                hover_background Solid("#f4e4bc30")
                action Return(nom)
                activate_sound "audio/clic.ogg"
                tooltip nom

    # L'énigme, en haut de l'écran
    frame:
        at panneau_apparait
        xalign 0.5
        ypos 20
        xmaximum 1300
        background Solid(gm_gold)
        padding (3, 3)
        frame:
            background Solid(gm_night)
            padding (30, 18)
            vbox:
                spacing 10
                text enigme["riddle"] color gm_parchemin size tx(30) xalign 0.5 text_align 0.5
                if indice_dispo:
                    text ("{i}Indice : " + enigme["indice"] + "{/i}") size tx(24) color gm_gold_light xalign 0.5 text_align 0.5
                text "Cliquez sur l'objet, dans la pièce." size tx(21) color gm_parchemin_sombre xalign 0.5
                use actions_enigme(sablier_dispo, implorer_dispo)

    # Nom de l'objet survolé
    $ survol = GetTooltip()
    if survol:
        frame:
            xalign 0.5
            yalign 0.97
            background Solid("#0d1524dd")
            padding (24, 8)
            text survol.capitalize() style "gm_titre" size tx(30) color gm_gold_light


# --- HUD (haut droite) : porte en cours, carte, pouvoirs ---
# Au-dessus du voile des écrans de choix, pour rester lisible.
screen hud_jeu():
    zorder 210

    vbox:
        at voile_apparait
        xalign 0.985
        yalign 0.025
        spacing 8

        hbox:
            xalign 1.0
            spacing 12

            frame:
                background Solid("#0d1524dd")
                padding (14, 6)
                hbox:
                    spacing 10
                    add "images/ui/icone_cle.webp" zoom 0.42 yalign 0.5
                    text ("Porte %d" % max(manche, 1)) style "gm_titre" size 28 color gm_gold yalign 0.5

            # La bougie : sa cire fond au fil des portes
            $ restantes_hud = portes_restantes()
            frame:
                background Solid("#0d1524dd")
                padding (14, 6)
                hbox:
                    spacing 10
                    fixed:
                        xysize (34, 48)
                        yalign 0.5
                        # cire (hauteur proportionnelle aux portes restantes)
                        $ cire = max(4, int(30 * restantes_hud / float(max_manches)))
                        add Solid("#e8dcc0") xysize (12, cire) xalign 0.5 yalign 1.0
                        if restantes_hud > 0:
                            add Transform("images/ui/flamme.webp", zoom=0.2) at flamme_vacille xpos 17 ypos (48 - cire)
                    text ("Bougie : %d" % restantes_hud) style "gm_titre" size 28 color (gm_gold if restantes_hud > 2 else "#d0584a") yalign 0.5

            button:
                background Solid("#0d1524dd")
                hover_background Solid(gm_bordeaux)
                padding (14, 6)
                action Show("carte_puzzle")
                hbox:
                    spacing 10
                    add "images/ui/icone_carte.webp" zoom 0.5 yalign 0.5
                    text ("Carte %d/%d" % (len(pieces_owned), total_pieces)) style "gm_titre" size 28 color gm_gold hover_color gm_gold_light yalign 0.5

        if pieces_owned:
            frame:
                xalign 1.0
                background Solid("#0d1524bb")
                padding (14, 4)
                text ("Pouvoirs : " + ", ".join(fragments[p]["pouvoir"] for p in sorted(pieces_owned) if not (p == "piece_04" and cle_utilisee))) size 22 color gm_parchemin


# --- Carte en cours de reconstitution, et notes au dos des fragments ---
screen carte_puzzle():
    modal True
    zorder 250

    add Solid("#000000bb") at voile_apparait

    use gm_panel(pad=40):
        vbox:
            spacing 22

            text "Le plan du manoir Blackwood" style "gm_titre" size 38 xalign 0.5

            hbox:
                spacing 40

                $ echelle = min(600.0 / map_full_width, 600.0 / map_full_height)
                fixed:
                    xysize (int(map_full_width * echelle), int(map_full_height * echelle))
                    add Solid("#1a2236")
                    for pid, pp in sorted(map_pieces_positions.items()):
                        $ morceau = Transform("images/map/" + pid + ".jpg", xysize=(int(pp["width"] * echelle), int(pp["height"] * echelle)))
                        if pid in pieces_owned:
                            add morceau xpos int(pp["x"] * echelle) ypos int(pp["y"] * echelle)
                        else:
                            # Fragment encore perdu : une zone de brouillard
                            add morceau at fragment_brouille xpos int(pp["x"] * echelle) ypos int(pp["y"] * echelle)
                            text "?" style "gm_titre" size 90 color "#c9a24a88" xanchor 0.5 yanchor 0.5 xpos int((pp["x"] + pp["width"] / 2) * echelle) ypos int((pp["y"] + pp["height"] / 2) * echelle)

                vbox:
                    xsize 560
                    spacing 16
                    text "Notes au dos des fragments" style "gm_titre" size 28 color gm_gold
                    for pid in sorted(pieces_owned):
                        vbox:
                            spacing 2
                            text fragments[pid]["nom"] style "gm_titre" size 23 color gm_gold_light
                            text fragments[pid]["lore"] italic True size 22 color gm_parchemin
                    if len(pieces_owned) < total_pieces:
                        text "D'autres notes attendent sur les morceaux perdus…" italic True size 21 color "#8a7f6a"

            textbutton "Fermer" action Hide("carte_puzzle") xalign 0.5 text_style "gm_titre" text_color gm_gold text_hover_color gm_gold_light text_size 28


## ------------------------------------------------------------
## ÉCRAN TITRE
## ------------------------------------------------------------

screen main_menu():
    tag menu

    add "bg_title"

    add Transform("images/ui/logo_title.jpg", xysize=(760, 520), fit="contain") at voile_apparait xalign 0.5 ypos 30

    vbox:
        xalign 0.5
        ypos 560
        spacing 14

        use gm_bouton("Commencer", Start(), 420, 80, 32, "btn_start", d=0.4)
        use gm_bouton("Charger", ShowMenu("load"), 420, 80, 32, "btn_load", d=0.55)
        use gm_bouton("Secrets du manoir", ShowMenu("secrets"), 420, 80, 30, "btn_load", d=0.7)
        use gm_bouton("Réglages", ShowMenu("preferences"), 420, 80, 32, "btn_load", d=0.85)
        use gm_bouton("Quitter", Quit(confirm=True), 420, 80, 32, "btn_quit", d=1.0)

    # Ce que le joueur a découvert (gardé d'une partie à l'autre)
    frame:
        at voile_apparait
        xpos 30
        yalign 0.97
        background Solid("#0d1524cc")
        padding (20, 12)
        vbox:
            spacing 4
            text ("Fins découvertes : %d/%d" % (len([f for f in fins if f[0] in persistent.fins_vues]), len(fins))) style "gm_titre" size 26 color gm_gold
            text ("Journal d'Éléonore : %d/%d pages" % (len(persistent.pages_journal), len(pages_journal))) style "gm_titre" size 26 color gm_gold


## ------------------------------------------------------------
## SECRETS DU MANOIR : fins, journal d'Éléonore, galerie
## ------------------------------------------------------------

define galerie_fonds = [
    ("bg_exterior_forest", "La forêt"), ("bg_manor_facade", "Le manoir"),
    ("bg_entrance_hall", "Le hall"), ("bg_corridor_01", "La galerie des portraits"),
    ("bg_corridor_02", "Le couloir au miroir"), ("bg_stairs", "L'escalier"),
    ("bg_attic", "Le grenier"), ("bg_cellar", "La cave"),
    ("bg_door_level_0", "La porte de chêne"), ("bg_door_level_1", "La porte gravée"),
    ("bg_door_level_2", "La porte aux runes"), ("bg_door_generic", "La porte de sortie"),
    ("bg_library", "La bibliothèque"), ("bg_secret_room", "La chambre d'Éléonore"),
    ("bg_victory", "L'aube"), ("bg_gameover", "La nuit sans fin"),
]

screen secrets():
    tag menu
    default onglet = "fins"
    default agrandi = None

    use game_menu(_("Secrets du manoir")):
        vbox:
            spacing 20
            xsize 1400

            hbox:
                style_prefix "gm_nav"
                xalign 0.5
                spacing 50
                textbutton "Fins" action SetScreenVariable("onglet", "fins")
                textbutton "Journal d'Éléonore" action SetScreenVariable("onglet", "journal")
                textbutton "Galerie" action SetScreenVariable("onglet", "galerie")

            viewport:
                xysize (1400, 600)
                scrollbars "vertical"
                mousewheel True
                draggable True

                if onglet == "fins":
                    vbox:
                        spacing 18
                        xsize 1360
                        for code, nom, piste in fins:
                            vbox:
                                spacing 2
                                if code in persistent.fins_vues:
                                    text ("« " + nom + " »") style "gm_titre" size tx(30) color gm_gold
                                    text piste size tx(23) color gm_parchemin
                                else:
                                    text "« ??? »" style "gm_titre" size tx(30) color "#6b6456"
                                    text ("Piste : " + piste) italic True size tx(23) color gm_parchemin_sombre

                elif onglet == "journal":
                    vbox:
                        spacing 18
                        xsize 1360
                        for i, page in enumerate(pages_journal):
                            if i in persistent.pages_journal:
                                text ("{b}Page %d.{/b} « %s »" % (i + 1, page)) size tx(25) color gm_parchemin
                            else:
                                text ("{b}Page %d.{/b} Cette page n'a pas encore été retrouvée." % (i + 1)) italic True size tx(25) color "#6b6456"

                else:
                    vpgrid:
                        cols 4
                        spacing 20
                        for nom_img, titre in galerie_fonds:
                            if renpy.has_image(nom_img) and renpy.seen_image(nom_img):
                                button:
                                    xysize (325, 200)
                                    padding (3, 3)
                                    background Solid(gm_gold)
                                    hover_background Solid(gm_gold_light)
                                    action SetScreenVariable("agrandi", nom_img)
                                    vbox:
                                        add Transform(nom_img, xysize=(319, 160), fit="cover")
                                        text titre size 20 color gm_encre xalign 0.5
                            else:
                                frame:
                                    xysize (325, 200)
                                    background Solid("#1a2236")
                                    text "?" style "gm_titre" size 70 color "#c9a24a55" align (0.5, 0.5)

    # Une illustration de la galerie en plein écran
    if agrandi:
        button:
            xfill True
            yfill True
            background Solid("#000000")
            action SetScreenVariable("agrandi", None)
            add agrandi
        text "Cliquez pour fermer" size 22 color gm_parchemin_sombre xalign 0.5 yalign 0.98


## ------------------------------------------------------------
## MENU DE JEU (conteneur Sauvegarder / Charger / Réglages / Historique)
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
                text title style "gm_titre" size 38 xalign 0.5
                transclude

    use navigation


style gm_nav_button is default
style gm_nav_button_text is gm_titre:
    size 28
    color "#c9a24a"
    hover_color "#f4e4bc"
    selected_color "#f4e4bc"

screen navigation():
    hbox:
        style_prefix "gm_nav"
        align (0.5, 0.95)
        spacing 40

        textbutton "Retour" action Return()
        if not main_menu:
            textbutton "Historique" action ShowMenu("history")
            textbutton "Sauvegarder" action ShowMenu("save")
        textbutton "Charger" action ShowMenu("load")
        textbutton "Réglages" action ShowMenu("preferences")
        if not main_menu:
            textbutton "Menu principal" action MainMenu(confirm=True)


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
                            text FileSlotName(i) style "gm_titre" color gm_gold size 22
                            text FileTime(i, format=_("%d/%m/%Y - %H:%M"), empty=_("Emplacement vide")) color gm_parchemin size 20


## ------------------------------------------------------------
## HISTORIQUE DES DIALOGUES
## ------------------------------------------------------------

screen history():
    tag menu
    predict False

    use game_menu(_("Historique")):
        viewport:
            xysize (1300, 640)
            scrollbars "vertical"
            mousewheel True
            draggable True
            yinitial 1.0

            vbox:
                spacing 16
                xsize 1260

                if not _history_list:
                    text "Rien à relire pour l'instant." size 26 color gm_parchemin_sombre

                for h in _history_list:
                    text h.what substitute False size 27 color gm_parchemin xsize 1240


## ------------------------------------------------------------
## RÉGLAGES (son et texte)
## ------------------------------------------------------------

screen preferences():
    use game_menu(_("Réglages")):
        vbox:
            spacing 25
            xsize 700

            for titre, reglage in [("Ambiance", "music volume"), ("Effets sonores", "sound volume")]:
                vbox:
                    spacing 8
                    text titre style "gm_titre" color gm_gold size 28
                    bar value Preference(reglage) xsize 700 ysize 30 left_bar Solid(gm_gold) right_bar Solid("#1a2236") thumb None

            vbox:
                spacing 8
                text "Vitesse du texte" style "gm_titre" color gm_gold size 28
                bar value Preference("text speed") xsize 700 ysize 30 left_bar Solid(gm_gold) right_bar Solid("#1a2236") thumb None

            textbutton "Couper tous les sons" action Preference("all mute", "toggle") text_style "gm_titre" text_color gm_gold text_hover_color gm_gold_light text_selected_color gm_gold_light text_size 26

            # Accessibilité
            text "Accessibilité" style "gm_titre" color gm_gold size 28
            hbox:
                spacing 40
                textbutton ("☑ Texte agrandi" if persistent.texte_grand else "☐ Texte agrandi") action ToggleField(persistent, "texte_grand") text_font "DejaVuSans.ttf" text_color gm_parchemin text_hover_color gm_gold_light text_size 26
                textbutton ("☑ Sans flash ni secousse" if persistent.sans_flash else "☐ Sans flash ni secousse") action ToggleField(persistent, "sans_flash") text_font "DejaVuSans.ttf" text_color gm_parchemin text_hover_color gm_gold_light text_size 26


## ------------------------------------------------------------
## CONFIRMATION (Quitter, Menu principal...)
## ------------------------------------------------------------

screen confirm(message, yes_action, no_action):
    modal True
    zorder 300

    add Solid("#000000cc") at voile_apparait

    use gm_panel(pad=40):
        vbox:
            spacing 30

            text message color gm_parchemin size 30 xsize 700 text_align 0.5 xalign 0.5

            hbox:
                xalign 0.5
                spacing 30
                use gm_bouton("Oui", yes_action, 200, 70, 28, "btn_start")
                use gm_bouton("Non", no_action, 200, 70, 28, "btn_quit")


## ------------------------------------------------------------
## NOTIFICATION (renpy.notify : fragment gagné...)
## ------------------------------------------------------------

screen notify(message):
    zorder 400

    frame:
        at notif_apparait
        xalign 0.5
        ypos 40
        background Solid(gm_gold)
        padding (3, 3)
        frame:
            background Solid(gm_night)
            padding (36, 14)
            hbox:
                spacing 14
                add "images/ui/icone_carte.webp" zoom 0.5 yalign 0.5
                text message style "gm_titre" size 30 color gm_gold_light yalign 0.5

    timer 2.8 action Hide("notify")
