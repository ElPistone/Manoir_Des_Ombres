########################################
# LE MANOIR-LABYRINTHE — script.rpy
# Logique principale du jeu
########################################

# --- Personnages ---
# ctc : petit triangle qui pulse en fin de texte, « cliquez pour continuer »
define narrateur = Character(
    None,
    what_color="#e8dcc0",
    ctc=At(Text("▼", size=20, color="#3b1524"), clignote),
    ctc_position="nestled",
)

# --- Écran titre ---
label start:

    play music "audio/ambiance_orage.ogg" fadein 2.0 volume 0.9
    scene bg_exterior_forest with fondu_lent
    narrateur "La pluie a effacé le chemin depuis longtemps. Vous êtes perdu, seul, dans la forêt."
    play sound "audio/tonnerre.ogg"
    narrateur "Le tonnerre gronde au loin, et vos vêtements trempés collent à votre peau. Continuer ainsi n'est plus possible."

    scene bg_manor_facade with fondu_lent
    narrateur "Au détour d'un sentier, un manoir se dresse, ses fenêtres hautes noyées d'obscurité, à l'exception d'une seule lueur vacillante."
    narrateur "Vous n'avez pas vraiment le choix : la nuit est trop noire, et la pluie trop froide, pour continuer."

    play sound "audio/porte_grince.ogg"
    scene bg_entrance_hall with fondu_lent
    play music "audio/ambiance_manoir.ogg" fadeout 2.0 fadein 3.0 volume 0.55
    narrateur "La porte s'ouvre sans résistance, comme si elle vous attendait. Elle se referme derrière vous, et vous comprenez qu'elle ne se rouvrira pas."

    if renpy.has_image("bg_fragment_floor"):
        scene bg_fragment_floor with fondu_lent
    play sound "audio/parchemin.ogg"
    narrateur "Sous le tapis de l'entrée dépasse un parchemin déchiré. Vous le ramassez : un morceau de carte, rien qu'un."

    $ pieces_owned = ["piece_01"]
    $ score = 0
    $ niveau = 0

    show screen hud_jeu

    narrateur "Une voix s'élève des murs : « Trois portes te séparent de la sortie. À chacune, tu offriras un morceau de ta carte. »"
    narrateur "« Réponds juste, et je te le rends, avec un autre. Trompe-toi une seule fois, et tu resteras ici. Pour toujours. »"

    jump door_loop


# --- Boucle principale : une itération par porte ---
label door_loop:

    # Victoire : les trois portes franchies d'affilée
    if niveau >= serie_requise:
        jump victory

    $ porte = portes[niveau]
    $ enigme_courante, choix_melanges = tirer_enigme(niveau)

    # Ambiance de transition (sauf avant la toute première porte)
    if niveau > 0:
        narrateur "[texte_aleatoire(ambiance_transitions)]"

    # Dernière porte : la musique se tend, un cœur bat
    if niveau == serie_requise - 1:
        play music "audio/ambiance_tension.ogg" fadeout 2.0 fadein 2.0 volume 0.6

    scene expression fond_porte(porte) with fondu_noir
    narrateur "[porte['intro']]"

    # Le joueur choisit quel morceau de carte il mise derrière cette porte
    call screen choix_piece(pieces_owned)
    $ piece_mise = _return

    # Le fragment choisi glisse sous la porte
    play sound "audio/parchemin.ogg"
    show expression ("images/map/%s.jpg" % piece_mise) as fragment_mise at fragment_glisse
    narrateur "[texte_aleatoire(messages_mise)]"
    hide fragment_mise

    # Question à choix multiples
    call screen menu_enigme(enigme_courante["riddle"], choix_melanges)
    $ choix_joueur = _return

    # La réponse est définitive : aucun retour en arrière possible
    $ renpy.block_rollback()

    if choix_joueur == enigme_courante["answer"]:
        $ score += porte["points"]
        $ pieces_owned.append(porte["reward_piece"])
        $ niveau += 1
        play sound "audio/bonne_reponse.ogg"
        with eclat_or
        $ renpy.notify("Nouveau fragment de carte : %d/%d" % (len(pieces_owned), total_pieces))
        narrateur "[texte_aleatoire(messages_victoire_porte)]"
        play sound "audio/porte_grince.ogg"
        narrateur "Score : [score] — Morceaux de carte : [len(pieces_owned)]/[total_pieces]"
        jump door_loop
    else:
        $ pieces_owned.remove(piece_mise)
        play sound "audio/mauvaise_reponse.ogg"
        with eclat_rouge
        with hpunch
        narrateur "[texte_aleatoire(messages_defaite_porte)]"
        jump defeat


# --- Fins ---
label victory:
    hide screen hud_jeu
    stop music fadeout 2.0
    play sound "audio/victoire.ogg"
    scene bg_victory with fin_partie
    narrateur "Les [total_pieces] morceaux, enfin réunis, s'assemblent sous vos yeux en une carte complète, ses lignes d'encre dorée traçant un chemin qui, l'instant d'avant, n'existait pas."
    narrateur "Le manoir semble retenir son souffle une dernière fois — puis, quelque part, une porte que vous n'aviez jamais remarquée s'ouvre sur la nuit finissante."
    narrateur "Vous sortez alors que le ciel, à l'est, commence à pâlir. Derrière vous, le manoir reprend son silence, comme s'il n'avait jamais eu de visiteur."
    narrateur "Score final : [score]."
    return


label defeat:
    hide screen hud_jeu
    stop music fadeout 1.5
    play sound "audio/defaite.ogg"
    scene bg_gameover with fin_partie
    narrateur "« Une seule erreur suffisait. » La voix ne gronde plus ; elle semble presque désolée."
    narrateur "Les morceaux qui vous restaient s'effritent entre vos doigts. Autour de vous, les couloirs se referment un à un — non pas dans un vacarme de pierre, mais dans un silence total, presque poli."
    play sound "audio/bougie_souffle.ogg"
    narrateur "La dernière chose que vous voyez est la lumière de votre bougie, qui vacille, puis s'éteint."
    narrateur "Portes franchies : [niveau]/[serie_requise]. Score final : [score]."
    return
