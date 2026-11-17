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
default indice_achete = False
default correct = False
default etape = 1


init python:

    def nouvelle_enigme(sauf=None):
        """Tire l'énigme de la porte en cours selon son type (sortie, porte
        qui murmure ou porte de chêne) et prépare le pouvoir de l'Encre."""
        if sortie:
            e, c = tirer_enigme(niveau_sortie, enigmes_vues, sauf=sauf)
        elif porte_murmure:
            e, c = tirer_murmure(niveau, enigmes_vues, salle_courante, sauf=sauf)
        else:
            e, c = tirer_enigme(niveau, enigmes_vues, sauf=sauf, salle=salle_courante)
        store.enigme_courante = e
        store.choix_melanges = c
        store.enigmes_vues.append(e["riddle"])
        store.barree = reponse_barree(e, c) if ("Encre" in actifs and not e.get("saisie")) else None

    def indice_visible():
        return "Lanterne" in actifs or indice_achete

    def implorer_possible():
        return not indice_visible() and portes_restantes() >= 1


# --- Introduction ---
label start:

    $ _game_menu_screen = "save"
    $ persistent.parties += 1
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
    $ salle_courante = "bg_entrance_hall"
    $ bonus_bougie = 0
    $ carte_complete_vue = False
    $ serie_ok = 0
    $ serie_ko = 0
    $ id_partie = "%08x" % renpy.random.getrandbits(32)

    $ lore_depart = fragments["piece_01"]["lore"]
    narrateur "Au dos, quelques lignes d'une écriture fine : [lore_depart]"

    show screen hud_jeu

    # Le manoir se souvient de ceux qui sont déjà venus
    if persistent.parties > 1:
        if persistent.derniere_fin in ("delivrance", "aube", "vrai_nom"):
            narrateur "Une voix de femme s'élève des murs, incrédule : « Toi ? Tu étais sorti… Pourquoi reviens-tu ? »"
        elif persistent.derniere_fin is not None:
            narrateur "Une voix de femme s'élève des murs : « Encore toi. La dernière fois, tu es resté avec moi. Tu t'en souviens ? »"
        else:
            narrateur "Une voix de femme s'élève des murs : « Je reconnais ton pas. Tu es déjà venu ici. »"
        $ texte_visite = "« C'est ta %de visite. Les murs se souviennent de toi, et moi aussi. »" % persistent.parties
        narrateur "[texte_visite]"
        narrateur "« Les règles n'ont pas changé. Il te faut [total_pieces] morceaux pour retrouver ton chemin. »"
    else:
        narrateur "Une voix de femme s'élève des murs : « Il te faut [total_pieces] morceaux pour retrouver ton chemin. À chaque porte, tu m'en offriras un. »"
    narrateur "« Réponds juste, et je te le rends, avec un autre. Trompe-toi, et je le garde. »"
    narrateur "« Chaque morceau a son pouvoir. Celui-ci est la Lanterne : tant que tu le gardes, je te soufflerai un indice. »"
    narrateur "« Mais le morceau que tu mises reste sous la porte… et son pouvoir avec lui. »"
    narrateur "« Dans chaque pièce, deux portes. Celle de chêne te proposera des réponses. Celle qui murmure t'obligera à chercher seul… mais elle sait se montrer généreuse. »"
    narrateur "« Ta bougie éclairera [max_manches] portes. Quand ta carte sera complète, il te restera la porte de sortie. Et si ta bougie s'éteint, ou si tes mains sont vides avant… tu resteras ici. Avec moi. »"

    jump door_loop


# --- Une page du journal d'Éléonore (gardée d'une partie à l'autre) ---
label trouver_une_page(intro=""):
    $ num_page = trouver_page()
    if num_page is None:
        return
    play sound "audio/parchemin.ogg"
    $ texte_page = "%s Une page du journal d'Éléonore (%d/%d)." % (intro, num_page, len(pages_journal))
    narrateur "[texte_page]"
    $ texte_page = "« %s »" % pages_journal[num_page - 1]
    narrateur "[texte_page]"
    if journal_complet():
        narrateur "Le journal est complet. Une phrase, sur la dernière page, semble écrite pour vous."
    return


# --- Boucle principale : une itération par porte (manche) ---
label door_loop:

    # Défaite : plus rien à miser, ou la bougie s'est éteinte
    if not pieces_owned or portes_restantes() <= 0:
        jump defeat

    $ manche += 1
    $ sortie = len(pieces_owned) >= total_pieces
    if sortie:
        $ carte_complete_vue = True
    # La difficulté suit le nombre de fragments ; la carte complète mène à la sortie
    $ niveau = niveau_sortie if sortie else min(len(pieces_owned) - 1, 2)
    $ porte = portes[niveau]
    $ sablier_utilise = False
    $ indice_achete = False
    $ porte_murmure = False
    $ etape = 1

    # Entre deux portes, on traverse une pièce du manoir
    if manche > 1:
        $ derniere_salle, texte_salle = tirer_salle(derniere_salle)
        $ salle_courante = derniere_salle
        scene expression derniere_salle with fondu_noir
        narrateur "[texte_salle]"
        # Parfois, une page du journal traîne dans la pièce
        if renpy.random.random() < 0.25:
            call trouver_une_page("Entre deux lattes du plancher, une feuille arrachée dépasse.")

    # Près du but (dernière porte ou sortie), la musique se tend
    if niveau >= 2:
        $ renpy.music.play("audio/ambiance_tension.ogg", fadeout=2.0, fadein=2.0, if_changed=True, relative_volume=0.6)
    else:
        $ renpy.music.play("audio/ambiance_manoir.ogg", fadeout=2.0, fadein=2.0, if_changed=True, relative_volume=0.55)

    # Partie rechargée après avoir répondu à cette porte : le verdict est déjà rendu
    $ verdict = verdict_connu()
    if verdict is not None:
        $ correct, mise = verdict[0], verdict[1]
        $ porte_murmure = verdict[2] if len(verdict) > 2 else False
        scene expression fond_porte(porte) with fondu_noir
        narrateur "« Tu as déjà répondu à cette porte », chuchote la voix. « Le manoir n'oublie rien. »"
        jump resolution

    # Pas de sauvegarde pendant le choix de la porte, la mise et l'énigme
    $ _game_menu_screen = None

    # Deux portes dans chaque pièce (sauf pour la sortie)
    if not sortie:
        call screen choix_porte(salle_courante, portes_restantes())
        $ porte_murmure = _return

    scene expression fond_porte(porte) with fondu_noir
    if porte_murmure:
        $ intro_porte = texte_aleatoire(voix_murmure)
    else:
        $ intro_porte = texte_aleatoire(porte["intros"])
    narrateur "[intro_porte]"

    # Le joueur choisit le ou les fragments qu'il mise derrière cette porte
    $ double_possible = (not sortie) and len(pieces_owned) >= 2 and len(pieces_owned) + 2 <= total_pieces
    call screen choix_piece(pieces_owned, double_possible, sortie)
    $ mise = list(_return)

    if len(mise) == 2:
        $ niveau = min(niveau + 1, 2)
        narrateur "La voix éclate d'un rire bref : « Deux d'un coup ? Alors l'énigme sera à la hauteur de ton audace. »"

    # Le fragment choisi glisse sous la porte
    play sound "audio/parchemin.ogg"
    show expression ("images/map/%s.jpg" % mise[0]) as fragment_mise at fragment_glisse(0.5 if len(mise) == 1 else 0.42)
    if len(mise) == 2:
        show expression ("images/map/%s.jpg" % mise[1]) as fragment_mise_2 at fragment_glisse(0.58)
    $ texte_mise = texte_aleatoire(messages_mise)
    narrateur "[texte_mise]"
    hide fragment_mise
    hide fragment_mise_2

    # La voix commente le pouvoir qu'on lui abandonne (une fois sur deux)
    if len(mise) == 1 and renpy.random.random() < 0.5:
        $ texte_voix = texte_aleatoire(voix_mise[fragments[mise[0]]["pouvoir"]])
        narrateur "[texte_voix]"

    # Pouvoirs des fragments restés en main, puis l'énigme
    $ actifs = pouvoirs_actifs(pieces_owned, mise)
    $ nouvelle_enigme()

    if sortie:
        narrateur "La porte de sortie porte deux verrous. Chacun attend sa réponse."

label poser_enigme:

    if enigme_courante.get("fouille"):
        # Fouille : on cherche l'objet dans la pièce elle-même
        scene expression salle_courante with dissolve
        call screen fouille_salle(enigme_courante, barree, indice_visible(), ("Sablier" in actifs and not sablier_utilise), implorer_possible())
    else:
        call screen menu_enigme(enigme_courante, choix_melanges, actifs, barree, ("Sablier" in actifs and not sablier_utilise), indice_visible(), implorer_possible())

    # Pouvoir du Sablier : une autre énigme du même type
    if _return == "__sablier__":
        $ sablier_utilise = True
        play sound "audio/parchemin.ogg"
        $ nouvelle_enigme(sauf=enigme_courante)
        narrateur "Vous retournez le sablier. Le sable remonte, et l'énigme se réécrit sous vos yeux."
        jump poser_enigme

    # Indice imploré : la bougie raccourcit d'une porte
    if _return == "__implorer__":
        $ indice_achete = True
        $ bonus_bougie -= 1
        play sound "audio/bougie_souffle.ogg"
        narrateur "Vous implorez la voix. La flamme de votre bougie se tord et rapetisse. « Écoute bien, car je ne le dirai qu'une fois… »"
        jump poser_enigme

    # Réponse libre vide (Entrée par mégarde) : on repose la question
    if enigme_courante.get("saisie") and not (_return or "").strip():
        jump poser_enigme

    $ choix_joueur = _return

    # Le nom de la voix, prononcé devant la porte de sortie
    if sortie and dit_le_nom(choix_joueur):
        if journal_complet():
            jump fin_vrai_nom
        narrateur "Les runes se figent. « Qui t'a dit mon nom ? » Un long silence. « Tu ne connais pas encore toute mon histoire. Réponds à l'énigme. »"
        jump poser_enigme

    # La réponse est définitive : aucun retour en arrière possible
    $ renpy.block_rollback()

    # Le manoir garde la trace de chaque verdict (contre les rechargements)
    $ verdict = verdict_connu()
    if verdict is not None:
        $ correct, mise = verdict[0], verdict[1]
    else:
        $ correct = bonne_reponse(enigme_courante, choix_joueur)

        # Porte de sortie : il faut ouvrir les deux verrous
        if correct and sortie and etape < etapes_sortie:
            $ etape += 1
            play sound "audio/bonne_reponse.ogg"
            narrateur "Le premier verrou cède avec un claquement sec. « Un autre », souffle la voix. « Le dernier. »"
            $ sablier_utilise = False
            $ indice_achete = False
            $ nouvelle_enigme()
            jump poser_enigme

        $ memoriser_verdict(correct, mise, porte_murmure)

label resolution:

    $ _game_menu_screen = "save"
    $ actifs = pouvoirs_actifs(pieces_owned, mise)

    if correct:
        $ serie_ok += 1
        $ serie_ko = 0
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
        with flash(eclat_or)
        # La porte s'ouvre : on avance dans l'embrasure
        scene expression fond_porte(porte) at porte_s_ouvre
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

        # Récompense de la porte qui murmure
        if porte_murmure:
            $ bonus_bougie += 1
            narrateur "La flamme de votre bougie se redresse et grandit : la porte qui murmure vous offre une porte de plus."
            call trouver_une_page("Glissée dans l'entrebâillement de la porte, une feuille vous attend.")

        if serie_ok >= 3 and serie_ok % 3 == 0:
            $ texte_voix = texte_aleatoire(voix_serie_ok)
            narrateur "[texte_voix]"

        play sound "audio/porte_grince.ogg"

    else:
        $ erreurs += 1
        $ serie_ko += 1
        $ serie_ok = 0
        play sound "audio/mauvaise_reponse.ogg"
        with flash(eclat_rouge)

        if "Clé" in actifs and not cle_utilisee:
            # Pouvoir de la Clé : une erreur pardonnée par partie
            $ cle_utilisee = True
            narrateur "La porte reste close… mais le fragment de la Clé se met à briller dans votre main. L'offrande vous est rendue. La Clé, elle, s'est ternie : elle ne vous sauvera plus."
        else:
            python:
                for _p in mise:
                    if _p in pieces_owned:
                        pieces_owned.remove(_p)
            if not persistent.sans_flash:
                with hpunch
            $ texte_defaite = texte_aleatoire(messages_defaite_porte)
            narrateur "[texte_defaite]"
            if sortie:
                narrateur "« Presque », souffle la voix. « Ta carte est de nouveau incomplète. »"

        if serie_ko >= 2 and pieces_owned:
            $ texte_voix = texte_aleatoire(voix_serie_ko)
            narrateur "[texte_voix]"

    # Petit bilan avant la porte suivante
    if pieces_owned and portes_restantes() > 0:
        $ restantes = portes_restantes()
        $ texte_restantes = "Votre bougie n'éclairera plus qu'une porte." if restantes == 1 else "Votre bougie peut encore éclairer %d portes." % restantes
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

    $ texte_score = "Sortie trouvée en %d portes, avec %d erreur%s." % (manche, erreurs, "s" if erreurs > 1 else "")
    narrateur "[texte_score]"
    return


# Fin secrète : dire le nom de la voix à la porte de sortie, journal complet
label fin_vrai_nom:
    $ _game_menu_screen = "save"
    $ renpy.block_rollback()
    hide screen hud_jeu
    stop music fadeout 3.0
    $ debloquer_fin("vrai_nom")
    play sound "audio/bougie_souffle.ogg"
    scene bg_secret_room with fin_partie
    narrateur "« Éléonore. » Le nom tombe dans le silence comme une pierre au fond d'un puits."
    narrateur "Les runes de la porte s'éteignent. Puis, une à une, toutes les bougies du manoir."
    narrateur "« Personne… personne ne l'avait jamais dit », souffle la voix. Pour la première fois, elle ne vient pas des murs, mais de juste à côté de vous."
    play sound "audio/victoire.ogg"
    scene bg_victory with fin_partie
    narrateur "Quand vous franchissez la grille, le manoir derrière vous n'est plus qu'un tas de pierres mangées par le lierre, comme s'il était en ruine depuis cent ans."
    narrateur "Près de vous, quelqu'un regarde le ciel pâlir. Elle avait oublié sa couleur. Fin secrète : « Le vrai nom »."
    return


label defeat:
    $ _game_menu_screen = "save"
    hide screen hud_jeu
    stop music fadeout 1.5
    play sound "audio/defaite.ogg"
    scene bg_gameover with fin_partie
    if not pieces_owned and carte_complete_vue:
        $ debloquer_fin("gardien")
        narrateur "Vos mains sont vides. Il y a quelques portes encore, vous teniez pourtant la carte entière."
        narrateur "« Tu étais si près », murmure la voix. « Moi aussi, autrefois. »"
        narrateur "Une main froide se pose sur la vôtre, puis s'en va. Des pas légers s'éloignent vers l'entrée, et la grande porte s'ouvre… pour quelqu'un d'autre."
        narrateur "Désormais, c'est votre voix qui résonne dans les murs. Vous attendez le prochain voyageur."
        $ nom_fin = "Le gardien"
    elif not pieces_owned:
        $ debloquer_fin("mains_vides")
        narrateur "Vos mains sont vides. Il ne vous reste plus rien à offrir au manoir."
        narrateur "« Ne t'inquiète pas », dit la voix, presque tendre. « On s'habitue. Moi, je me suis habituée. »"
        $ nom_fin = "Les mains vides"
    else:
        $ debloquer_fin("minuit")
        narrateur "Votre bougie n'est plus qu'une flaque de cire. Quelque part, une horloge sonne le dernier coup de minuit, et votre carte ne vous mènera nulle part."
        $ nom_fin = "Le dernier coup de minuit"
    narrateur "Autour de vous, les couloirs se referment un à un, non pas dans un vacarme de pierre, mais dans un silence total, presque poli."
    play sound "audio/bougie_souffle.ogg"
    narrateur "La dernière chose que vous voyez est la lumière de votre bougie, qui vacille, puis s'éteint. Fin : « [nom_fin] »."
    $ texte_score = "Morceaux réunis : %d/%d." % (len(pieces_owned), total_pieces)
    narrateur "[texte_score]"
    return
