########################################
# LE MANOIR DES OMBRES — script.rpy
# Logique principale du jeu
########################################

# --- Personnages ---
# ctc : petit triangle qui pulse en fin de texte, « cliquez pour continuer »
# (DejaVuSans car la police du jeu n'a pas le caractère ▼)
define narrateur = Character(
    None,
    ctc=At(Text("▼", size=20, color="#5a0f1c", font="DejaVuSans.ttf"), clignote),
    ctc_position="nestled",
)

default derniere_salle = None
default sortie = False
default actifs = []
default barree = None
default sablier_utilise = False
default correct = False


# --- Introduction ---
label start:

    $ _game_menu_screen = "save"
    play music "audio/ambiance_orage.ogg" fadein 2.0 volume 0.9
    scene bg_exterior_forest with fondu_lent
    narrateur "La pluie a effacé le chemin depuis longtemps. Vous êtes perdu, seul, dans la forêt."
    play sound "audio/tonnerre.ogg"
    narrateur "Le tonnerre gronde au loin, et vos vêtements trempés collent à votre peau. Continuer ainsi n'est plus possible."

    scene bg_manor_facade with fondu_lent
    narrateur "Au détour d'un sentier, un manoir se dresse, ses fenêtres hautes noyées d'obscurité, à l'exception d'une seule lueur vacillante."
    narrateur "Sur la grille rouillée, une plaque à demi effacée : « Blackwood ». La nuit est trop noire, et la pluie trop froide, pour aller plus loin."

    play sound "audio/porte_grince.ogg"
    scene bg_entrance_hall with fondu_lent
    play music "audio/ambiance_manoir.ogg" fadeout 2.0 fadein 3.0 volume 0.55
    narrateur "La porte s'ouvre sans résistance, comme si elle vous attendait. Elle se referme derrière vous, et vous comprenez qu'elle ne se rouvrira pas."

    if renpy.has_image("bg_fragment_floor"):
        scene bg_fragment_floor with fondu_lent
    play sound "audio/parchemin.ogg"
    narrateur "Sous le tapis de l'entrée dépasse un parchemin déchiré. Vous le ramassez : un morceau de plan, rien qu'un."

    $ pieces_owned = ["piece_01"]
    $ manche = 0
    $ niveau = 0
    $ enigmes_vues = []
    $ mise = []
    $ erreurs = 0
    $ cle_utilisee = False
    $ derniere_salle = None
    $ id_partie = "%08x" % renpy.random.getrandbits(32)

    $ lore_depart = fragments["piece_01"]["lore"]
    narrateur "Au dos, quelques lignes d'une écriture fine : [lore_depart]"

    show screen hud_jeu

    narrateur "Une voix de femme s'élève des murs : « Il te faut [total_pieces] morceaux pour retrouver ton chemin. À chaque porte, tu m'en offriras un. »"
    narrateur "« Réponds juste, et je te le rends, avec un autre. Trompe-toi, et je le garde. »"
    narrateur "« Chaque morceau a son pouvoir. Celui-ci est la Lanterne : tant que tu le gardes, je te soufflerai un indice. »"
    narrateur "« Mais le morceau que tu mises reste sous la porte… et son pouvoir avec lui. »"
    narrateur "« Quand ta carte sera complète, il te restera la porte de sortie. [max_manches] portes, pas une de plus. Et si tes mains sont vides avant… tu resteras ici. Avec moi. »"

    jump door_loop


# --- Boucle principale : une itération par porte (manche) ---
label door_loop:

    # Défaite : plus rien à miser, ou toutes les portes passées
    if not pieces_owned or manche >= max_manches:
        jump defeat

    $ manche += 1
    $ sortie = len(pieces_owned) >= total_pieces
    # La difficulté suit le nombre de fragments ; la carte complète mène à la sortie
    $ niveau = niveau_sortie if sortie else min(len(pieces_owned) - 1, 2)
    $ porte = portes[niveau]
    $ sablier_utilise = False

    # Entre deux portes, on traverse une pièce du manoir
    if manche > 1:
        $ derniere_salle, texte_salle = tirer_salle(derniere_salle)
        scene expression derniere_salle with fondu_noir
        narrateur "[texte_salle]"

    # Près du but (dernière porte ou sortie), la musique se tend
    if niveau >= 2:
        $ renpy.music.play("audio/ambiance_tension.ogg", fadeout=2.0, fadein=2.0, if_changed=True, relative_volume=0.6)
    else:
        $ renpy.music.play("audio/ambiance_manoir.ogg", fadeout=2.0, fadein=2.0, if_changed=True, relative_volume=0.55)

    scene expression fond_porte(porte) with fondu_noir
    $ intro_porte = texte_aleatoire(porte["intros"])
    narrateur "[intro_porte]"

    # Partie rechargée après avoir répondu à cette porte : le verdict est déjà rendu
    $ verdict = verdict_connu()
    if verdict is not None:
        $ correct, mise = verdict
        narrateur "« Tu as déjà répondu à cette porte », chuchote la voix. « Le manoir n'oublie rien. »"
        jump resolution

    # Pas de sauvegarde pendant la mise et l'énigme
    $ _game_menu_screen = None

    # Le joueur choisit le ou les fragments qu'il mise derrière cette porte
    $ double_possible = (not sortie) and len(pieces_owned) >= 2 and len(pieces_owned) + 2 <= total_pieces
    call screen choix_piece(pieces_owned, double_possible, sortie)
    $ mise = list(_return)

    if len(mise) == 2:
        $ niveau = min(niveau + 1, 2)
        narrateur "La voix éclate d'un rire bref : « Deux d'un coup ? Alors l'énigme sera à la hauteur de ton audace. »"

    $ enigme_courante, choix_melanges = tirer_enigme(niveau, enigmes_vues)
    $ enigmes_vues.append(enigme_courante["riddle"])

    # Le fragment choisi glisse sous la porte
    play sound "audio/parchemin.ogg"
    show expression ("images/map/%s.jpg" % mise[0]) as fragment_mise at fragment_glisse(0.5 if len(mise) == 1 else 0.42)
    if len(mise) == 2:
        show expression ("images/map/%s.jpg" % mise[1]) as fragment_mise_2 at fragment_glisse(0.58)
    $ texte_mise = texte_aleatoire(messages_mise)
    narrateur "[texte_mise]"
    hide fragment_mise
    hide fragment_mise_2

    # Pouvoirs des fragments restés en main
    $ actifs = pouvoirs_actifs(pieces_owned, mise)
    $ barree = reponse_barree(enigme_courante, choix_melanges) if ("Encre" in actifs and not enigme_courante.get("saisie")) else None

label poser_enigme:

    call screen menu_enigme(enigme_courante, choix_melanges, actifs, barree, ("Sablier" in actifs and not sablier_utilise))

    # Pouvoir du Sablier : une autre énigme du même niveau
    if _return == "__sablier__":
        $ sablier_utilise = True
        play sound "audio/parchemin.ogg"
        $ enigme_courante, choix_melanges = tirer_enigme(niveau, enigmes_vues, sauf=enigme_courante)
        $ enigmes_vues.append(enigme_courante["riddle"])
        $ barree = reponse_barree(enigme_courante, choix_melanges) if ("Encre" in actifs and not enigme_courante.get("saisie")) else None
        narrateur "Vous retournez le sablier. Le sable remonte, et l'énigme se réécrit sous vos yeux."
        jump poser_enigme

    # Réponse libre vide (Entrée par mégarde) : on repose la question
    if enigme_courante.get("saisie") and not (_return or "").strip():
        jump poser_enigme

    $ choix_joueur = _return
    $ _game_menu_screen = "save"

    # La réponse est définitive : aucun retour en arrière possible
    $ renpy.block_rollback()

    # Le manoir garde la trace de chaque verdict (contre les rechargements)
    $ verdict = verdict_connu()
    if verdict is not None:
        $ correct, mise = verdict
    else:
        $ correct = bonne_reponse(enigme_courante, choix_joueur)
        $ memoriser_verdict(correct, mise)

label resolution:

    $ _game_menu_screen = "save"
    $ actifs = pouvoirs_actifs(pieces_owned, mise)

    if correct:
        if sortie:
            jump victory

        python:
            gagnes = []
            for _i in range(len(mise)):
                _p = prochaine_piece(pieces_owned)
                if _p:
                    pieces_owned.append(_p)
                    gagnes.append(_p)

        play sound "audio/bonne_reponse.ogg"
        with eclat_or
        $ texte_victoire = texte_aleatoire(messages_victoire_porte)
        narrateur "[texte_victoire]"

        # Chaque nouveau fragment : son pouvoir, puis la note écrite au dos
        $ i_gain = 0
        while i_gain < len(gagnes):
            $ _p = gagnes[i_gain]
            $ renpy.notify("%s (%d/%d)" % (fragments[_p]["nom"], len(pieces_owned), total_pieces))
            $ texte_gain = "Vous gagnez le %s. %s" % (fragments[_p]["nom"], fragments[_p]["effet"])
            narrateur "[texte_gain]"
            $ texte_lore = fragments[_p]["lore"]
            narrateur "Au dos, quelques lignes d'une écriture fine : [texte_lore]"
            $ i_gain += 1

        play sound "audio/porte_grince.ogg"

    else:
        $ erreurs += 1
        play sound "audio/mauvaise_reponse.ogg"
        with eclat_rouge

        if "Clé" in actifs and not cle_utilisee:
            # Pouvoir de la Clé : une erreur pardonnée par partie
            $ cle_utilisee = True
            narrateur "La porte reste close… mais le fragment de la Clé se met à briller dans votre main. L'offrande vous est rendue. La Clé, elle, s'est ternie : elle ne vous sauvera plus."
        else:
            python:
                for _p in mise:
                    if _p in pieces_owned:
                        pieces_owned.remove(_p)
            with hpunch
            $ texte_defaite = texte_aleatoire(messages_defaite_porte)
            narrateur "[texte_defaite]"
            if sortie:
                narrateur "« Presque », souffle la voix. « Ta carte est de nouveau incomplète. »"

    # Petit bilan avant la porte suivante
    if pieces_owned and manche < max_manches:
        $ restantes = max_manches - manche
        $ texte_restantes = "Il ne reste qu'une porte." if restantes == 1 else "Il reste %d portes." % restantes
        if len(pieces_owned) >= total_pieces:
            $ bilan = "La carte est complète ! Il ne reste qu'à trouver la porte de sortie. %s" % texte_restantes
        else:
            $ bilan = "Morceaux de carte : %d/%d. %s" % (len(pieces_owned), total_pieces, texte_restantes)
        narrateur "[bilan]"

    jump door_loop


# --- Fins ---
label victory:
    $ _game_menu_screen = "save"
    hide screen hud_jeu
    stop music fadeout 2.0
    play sound "audio/victoire.ogg"
    scene bg_victory with fin_partie
    narrateur "La porte de sortie cède. Les lignes d'encre dorée de la carte s'éteignent une à une : le chemin est parcouru."

    if erreurs == 0:
        # Fin « La délivrance » : aucune erreur de toute la partie
        $ debloquer_fin("delivrance")
        narrateur "Vous franchissez le seuil. Derrière vous, des pas légers suivent les vôtres, puis s'arrêtent sur la dernière marche."
        narrateur "« Merci », murmure la voix, si près que vous sentez un souffle sur votre nuque. « Cela faisait si longtemps que je n'avais pas vu l'aube. »"
        narrateur "Quand vous vous retournez, il n'y a personne. Seulement deux ombres sur l'herbe mouillée, et la vôtre est la seule à rester."
        narrateur "Éléonore Blackwood a enfin quitté le manoir. Fin : « La délivrance »."
    else:
        # Fin « L'aube »
        $ debloquer_fin("aube")
        narrateur "Vous sortez alors que le ciel, à l'est, commence à pâlir. Derrière vous, le manoir reprend son silence, comme s'il n'avait jamais eu de visiteur."
        narrateur "Au loin, une voix appelle encore, très bas : « Emmène-moi… » Mais la porte s'est déjà refermée. Fin : « L'aube »."
        narrateur "(Peut-être existe-t-il une autre fin, pour qui ne se tromperait jamais…)"

    $ texte_score = "Sortie trouvée en %d portes sur %d, avec %d erreur%s." % (manche, max_manches, erreurs, "s" if erreurs > 1 else "")
    narrateur "[texte_score]"
    return


label defeat:
    $ _game_menu_screen = "save"
    hide screen hud_jeu
    stop music fadeout 1.5
    play sound "audio/defaite.ogg"
    scene bg_gameover with fin_partie
    if not pieces_owned:
        $ debloquer_fin("mains_vides")
        narrateur "Vos mains sont vides. Il ne vous reste plus rien à offrir au manoir."
        narrateur "« Ne t'inquiète pas », dit la voix, presque tendre. « On s'habitue. Moi, je me suis habituée. »"
        $ nom_fin = "Les mains vides"
    else:
        $ debloquer_fin("minuit")
        narrateur "Quelque part, une horloge sonne le dernier coup de minuit. « [max_manches] portes, pas une de plus », rappelle la voix. Votre carte ne vous mènera nulle part."
        $ nom_fin = "Le dernier coup de minuit"
    narrateur "Autour de vous, les couloirs se referment un à un, non pas dans un vacarme de pierre, mais dans un silence total, presque poli."
    play sound "audio/bougie_souffle.ogg"
    narrateur "La dernière chose que vous voyez est la lumière de votre bougie, qui vacille, puis s'éteint. Fin : « [nom_fin] »."
    $ texte_score = "Morceaux réunis : %d/%d." % (len(pieces_owned), total_pieces)
    narrateur "[texte_score]"
    return
