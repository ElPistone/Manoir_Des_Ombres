########################################
# LE MANOIR-LABYRINTHE — textes.rpy
# Pools de dialogues/ambiance pour éviter la répétition sur 9 portes
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

    def texte_aleatoire(liste):
        """Retourne une entrée aléatoire d'une des listes ci-dessus."""
        return renpy.random.choice(liste)
