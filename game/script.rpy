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
    narrateur "La porte s'ouvre sans résistance, comme si elle vous attendait. À l'intérieur, un parchemin déchiré est glissé sous le tapis de l'entrée."
    narrateur "Vous le ramassez. Un seul morceau — mais un morceau de quoi, exactement, vous l'ignorez encore."

    $ pieces_owned = ["piece_01"]
    $ score = 0
    $ door_index = 0

    show screen hud_jeu

    narrateur "Un seul morceau de carte. Il en faudra [total_pieces] pour sortir d'ici... si vous en sortez."

    jump door_loop


# --- Boucle principale : une itération par porte ---
label door_loop:

    # Condition de victoire : toutes les pièces réunies
    if len(pieces_owned) >= total_pieces:
        jump victory

    # Condition de défaite : plus aucune pièce à miser
    if len(pieces_owned) == 0:
        jump defeat

    # Plus de portes disponibles mais carte incomplète
    if door_index >= len(doors_data):
        if len(pieces_owned) >= total_pieces:
            jump victory
        else:
            jump defeat

    $ current_door = doors_data[door_index]

    # Ambiance de transition (sauf avant la toute première porte)
    if door_index > 0:
        narrateur "[texte_aleatoire(ambiance_transitions)]"

    scene expression current_door["bg"] with dissolve
    narrateur "[current_door['intro']]"

    # Le joueur choisit quel morceau de carte il mise derrière cette porte
    call screen choix_piece(pieces_owned) with dissolve
    $ piece_mise = _return

    narrateur "[texte_aleatoire(messages_mise)]"

    # Question à choix multiples
    call screen menu_enigme(current_door["riddle"], current_door["choices"]) with dissolve
    $ choix_joueur = _return

    if choix_joueur == current_door["correct"]:
        $ score += 10
        $ pieces_owned.append(current_door["reward_piece"])
        narrateur "[texte_aleatoire(messages_victoire_porte)]"
        narrateur "Score : [score] — Morceaux de carte : [len(pieces_owned)]/[total_pieces]"
    else:
        $ pieces_owned.remove(piece_mise)
        $ score -= 5
        narrateur "[texte_aleatoire(messages_defaite_porte)]"
        narrateur "Score : [score] — Morceaux de carte : [len(pieces_owned)]/[total_pieces]"

    $ door_index += 1
    jump door_loop


# --- Fins ---
label victory:
    hide screen hud_jeu
    scene bg_victory with dissolve
    narrateur "Les dix morceaux, enfin réunis, s'assemblent sous vos yeux en une carte complète, ses lignes d'encre dorée traçant un chemin qui, l'instant d'avant, n'existait pas."
    narrateur "Le manoir semble retenir son souffle une dernière fois — puis, quelque part, une porte que vous n'aviez jamais remarquée s'ouvre sur la nuit finissante."
    narrateur "Vous sortez alors que le ciel, à l'est, commence à pâlir. Derrière vous, le manoir reprend son silence, comme s'il n'avait jamais eu de visiteur."
    narrateur "Score final : [score]."
    return


label defeat:
    hide screen hud_jeu
    scene bg_gameover with dissolve
    narrateur "Vos mains sont vides. Plus rien à offrir au manoir."
    narrateur "Autour de vous, les couloirs se referment un à un — non pas dans un vacarme de pierre, mais dans un silence total, presque poli."
    narrateur "La dernière chose que vous voyez est la lumière de votre bougie, qui vacille, puis s'éteint."
    narrateur "Score final : [score]."
    return
