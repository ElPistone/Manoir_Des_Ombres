########################################
# LE MANOIR DES OMBRES — textes.rpy
# Pools de dialogues/ambiance pour varier les textes d'une partie à l'autre
########################################

init python:

    # --- Quand le joueur mise un morceau de carte ---
    messages_mise = [
        "Vous glissez votre morceau de carte sous la porte, en offrande.",
        "Le morceau quitte votre main à contrecœur ; vous le poussez sous le battant de bois.",
        "Vous hésitez un instant, puis laissez le fragment de parchemin glisser dans l'obscurité sous la porte.",
        "Vos doigts tremblent légèrement en abandonnant le fragment à la fente sombre sous la porte.",
    ]

    # --- Bonne réponse ---
    messages_victoire_porte = [
        "La porte s'ouvre en grand ! Votre morceau vous est rendu, et un autre glisse vers vous depuis l'obscurité.",
        "Un déclic sec résonne dans le bois. La porte cède, et un nouveau morceau de parchemin tombe à vos pieds.",
        "Quelque chose, de l'autre côté, semble presque satisfait. La porte s'entrouvre, généreuse cette fois.",
        "Les symboles gravés s'illuminent brièvement d'or avant de s'éteindre. La porte s'ouvre sans un bruit.",
    ]

    # --- Mauvaise réponse ---
    messages_defaite_porte = [
        "Un rire sourd résonne. Le morceau est englouti par le manoir, à jamais perdu.",
        "La porte reste close. Sous vos pieds, le morceau de carte se dissout comme de l'encre dans l'eau.",
        "Un souffle glacé s'échappe sous la porte, emportant votre offrande avec lui.",
        "Le silence qui suit est pire que n'importe quel rire. Le morceau a disparu.",
    ]

    # --- Ambiance entre deux portes (affiché avant l'intro de la porte suivante) ---
    ambiance_transitions = [
        "Le silence du manoir n'est troublé que par le bruit de vos propres pas.",
        "Quelque part, une horloge égrène des heures qui ne devraient pas exister.",
        "L'air se fait plus froid à mesure que vous avancez.",
        "Une bougie s'éteint derrière vous, sans que rien ne l'ait soufflée.",
        "Vous avez l'impression, fugace, que les murs se sont légèrement déplacés.",
        "Un courant d'air porte une odeur de parchemin brûlé.",
    ]

    # --- Pièces traversées entre deux portes (un fond + un texte tirés au hasard) ---
    salles = [
        {"bg": "bg_attic", "textes": [
            "Un escalier étroit vous mène au grenier. Sous les draps, des meubles attendent un retour qui ne viendra pas.",
            "Dans le grenier, un fauteuil à bascule oscille encore doucement. Personne ne s'y est assis depuis des années.",
        ]},
        {"bg": "bg_cellar", "textes": [
            "La cave sent la terre humide et le vin tourné. Quelque chose a gratté les murs, de l'intérieur.",
            "Entre les tonneaux de la cave, une bougie brûle sans jamais raccourcir.",
        ]},
        {"bg": "bg_stairs", "textes": [
            "L'escalier en colimaçon tourne plus de fois qu'il ne devrait. Vous cessez de compter les marches.",
            "Vous descendez l'escalier de pierre, et pourtant vous arrivez à l'étage du dessus.",
        ]},
        {"bg": "bg_corridor_02", "textes": [
            "Dans le miroir du couloir, la pièce reflétée n'est pas tout à fait celle où vous vous tenez.",
            "Le couloir s'allonge à chaque pas. Dans le miroir, une silhouette en robe noire disparaît dès que vous la regardez.",
        ]},
        {"bg": "bg_corridor_01", "textes": [
            "Le silence du manoir n'est troublé que par le bruit de vos propres pas.",
            "Une bougie s'éteint derrière vous, sans que rien ne l'ait soufflée.",
        ]},
    ]

    def tirer_salle(derniere=None):
        """Une pièce au hasard (différente de la précédente) et son texte."""
        dispo = [s for s in salles if s["bg"] != derniere and renpy.has_image(s["bg"])] or salles
        salle = renpy.random.choice(dispo)
        return salle["bg"], renpy.random.choice(salle["textes"])

    def texte_aleatoire(liste):
        """Retourne une entrée aléatoire d'une des listes ci-dessus."""
        return renpy.random.choice(liste)
