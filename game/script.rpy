########################################
# LE MANOIR-LABYRINTHE — script.rpy
# Logique principale du jeu
########################################

# --- Personnages ---
define narrateur = Character(None, what_color="#e8dcc0")

# --- Écran titre ---
label start:

    scene bg_exterior_forest with dissolve
    narrateur "La pluie a effacé le chemin depuis longtemps. Vous êtes perdu, seul, dans la forêt."
    narrateur "Le tonnerre gronde au loin, et vos vêtements trempés collent à votre peau. Continuer ainsi n'est plus possible."

    scene bg_manor_facade with dissolve
    narrateur "Au détour d'un sentier, un manoir se dresse, ses fenêtres hautes noyées d'obscurité, à l'exception d'une seule lueur vacillante."
    narrateur "Vous n'avez pas vraiment le choix : la nuit est trop noire, et la pluie trop froide, pour continuer."

    scene bg_entrance_hall with dissolve
    narrateur "La porte s'ouvre sans résistance, comme si elle vous attendait. Elle se referme derrière vous, et vous comprenez qu'elle ne se rouvrira pas."

    if renpy.has_image("bg_fragment_floor"):
        scene bg_fragment_floor with dissolve
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

    scene expression fond_porte(porte) with dissolve
    narrateur "[porte['intro']]"

    # Le joueur choisit quel morceau de carte il mise derrière cette porte
    call screen choix_piece(pieces_owned) with dissolve
    $ piece_mise = _return

    narrateur "[texte_aleatoire(messages_mise)]"

    # Question à choix multiples
    call screen menu_enigme(enigme_courante["riddle"], choix_melanges) with dissolve
    $ choix_joueur = _return

    # La réponse est définitive : aucun retour en arrière possible
    $ renpy.block_rollback()

    if choix_joueur == enigme_courante["answer"]:
        $ score += porte["points"]
        $ pieces_owned.append(porte["reward_piece"])
        $ niveau += 1
        narrateur "[texte_aleatoire(messages_victoire_porte)]"
        narrateur "Score : [score] — Morceaux de carte : [len(pieces_owned)]/[total_pieces]"
        jump door_loop
    else:
        $ pieces_owned.remove(piece_mise)
        narrateur "[texte_aleatoire(messages_defaite_porte)]"
        jump defeat


# --- Fins ---
label victory:
    hide screen hud_jeu
    scene bg_victory with dissolve
    narrateur "Les [total_pieces] morceaux, enfin réunis, s'assemblent sous vos yeux en une carte complète, ses lignes d'encre dorée traçant un chemin qui, l'instant d'avant, n'existait pas."
    narrateur "Le manoir semble retenir son souffle une dernière fois — puis, quelque part, une porte que vous n'aviez jamais remarquée s'ouvre sur la nuit finissante."
    narrateur "Vous sortez alors que le ciel, à l'est, commence à pâlir. Derrière vous, le manoir reprend son silence, comme s'il n'avait jamais eu de visiteur."
    narrateur "Score final : [score]."
    return


label defeat:
    hide screen hud_jeu
    scene bg_gameover with dissolve
    narrateur "« Une seule erreur suffisait. » La voix ne gronde plus ; elle semble presque désolée."
    narrateur "Les morceaux qui vous restaient s'effritent entre vos doigts. Autour de vous, les couloirs se referment un à un — non pas dans un vacarme de pierre, mais dans un silence total, presque poli."
    narrateur "La dernière chose que vous voyez est la lumière de votre bougie, qui vacille, puis s'éteint."
    narrateur "Portes franchies : [niveau]/[serie_requise]. Score final : [score]."
    return
