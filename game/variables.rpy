########################################
# LE MANOIR-LABYRINTHE — variables.rpy
# Variables globales et données des énigmes
########################################

# Règle : le joueur doit réussir 3 énigmes D'AFFILÉE, de difficulté
# croissante (niveau 0 → 1 → 2). Une seule erreur et le manoir garde tout.
define serie_requise = 3
define total_pieces = 4           # le fragment du hall + un par porte franchie

default score = 0
default pieces_owned = []         # liste des pièces possédées, ex: ["piece_01", "piece_02"]
default niveau = 0                # porte actuelle = niveau de difficulté (0, 1, 2)
default enigme_courante = None    # énigme tirée pour la porte en cours
default choix_melanges = []       # réponses de l'énigme, dans un ordre aléatoire

init python:

    # Une porte par niveau : décor, texte d'arrivée et récompense.
    # "bg" est le fond dédié ; "bg_secours" sert tant qu'il n'existe pas.
    portes = [
        {
            "bg": "bg_door_level_0",
            "bg_secours": "bg_corridor_01",
            "intro": "Au bout du premier couloir, une porte de chêne toute simple vous attend, éclairée par une bougie posée sur un guéridon. Une voix douce, presque amusée, murmure à travers le bois.",
            "points": 10,
            "reward_piece": "piece_02",
        },
        {
            "bg": "bg_door_level_1",
            "bg_secours": "bg_library",
            "intro": "La deuxième porte se cache au fond de la bibliothèque, ses panneaux couverts de lettres gravées. L'air sent le vieux papier, et la voix, cette fois, ne sourit plus.",
            "points": 20,
            "reward_piece": "piece_03",
        },
        {
            "bg": "bg_door_level_2",
            "bg_secours": "bg_secret_room",
            "intro": "La dernière porte est noire, immense, striée de runes dorées qui pulsent comme un cœur. Derrière elle, vous le sentez, il y a la sortie. La voix gronde maintenant, grave et patiente.",
            "points": 40,
            "reward_piece": "piece_04",
        },
    ]

    # Énigmes classées par difficulté. Une est tirée au hasard pour chaque
    # porte, et ses réponses sont mélangées : "answer" est donc le TEXTE de
    # la bonne réponse, pas sa position.
    enigmes_par_niveau = [
        # --- Niveau 0 : volontairement très simple ---
        [
            {
                "riddle": "Je suis blanche, je tombe du ciel en hiver et je fonds au soleil. Qui suis-je ?",
                "choices": ["La neige", "La pluie", "Le sable", "La cendre"],
                "answer": "La neige",
            },
            {
                "riddle": "Je brille dans le ciel la nuit, et ma forme change au fil du mois. Qui suis-je ?",
                "choices": ["La lune", "Le soleil", "Un nuage", "Un oiseau"],
                "answer": "La lune",
            },
            {
                "riddle": "Je porte le nom de ma propre couleur, et l'on me mange en hiver. Quel fruit suis-je ?",
                "choices": ["L'orange", "La pomme", "La poire", "La fraise"],
                "answer": "L'orange",
            },
            {
                "riddle": "On me monte et on me descend, mais je ne bouge jamais. Qui suis-je ?",
                "choices": ["Un escalier", "Un ascenseur", "Un ballon", "Un cheval"],
                "answer": "Un escalier",
            },
        ],
        # --- Niveau 1 : il faut réfléchir ---
        [
            {
                "riddle": "Plus on m'enlève de matière, plus je deviens grand. Qui suis-je ?",
                "choices": ["Un trou", "Un mur", "Un arbre", "Une montagne"],
                "answer": "Un trou",
            },
            {
                "riddle": "Je suis plein de trous, et pourtant je retiens l'eau. Qui suis-je ?",
                "choices": ["Une éponge", "Un seau", "Un filet", "Une passoire"],
                "answer": "Une éponge",
            },
            {
                "riddle": "Plus je sèche, plus je suis mouillée. Qui suis-je ?",
                "choices": ["Une serviette", "Une éponge", "Un miroir", "Un livre"],
                "answer": "Une serviette",
            },
            {
                "riddle": "Il est à vous, mais les autres s'en servent bien plus que vous. Qu'est-ce que c'est ?",
                "choices": ["Votre prénom", "Votre maison", "Votre ombre", "Votre voix"],
                "answer": "Votre prénom",
            },
        ],
        # --- Niveau 2 : vraiment difficile, souvent un piège ---
        [
            {
                "riddle": "Celui qui me fabrique me vend. Celui qui m'achète ne se sert pas de moi. Celui qui se sert de moi ne me voit jamais. Qui suis-je ?",
                "choices": ["Un cercueil", "Un cadeau", "Une perruque", "Un miroir"],
                "answer": "Un cercueil",
            },
            {
                "riddle": "Le père d'Éléonore a cinq filles : Lala, Lélé, Lili et Lolo. Comment s'appelle la cinquième ?",
                "choices": ["Éléonore", "Lulu", "Lyly", "Lala"],
                "answer": "Éléonore",
            },
            {
                "riddle": "On me trouve deux fois dans « année », une fois dans « nuit », et jamais dans « jour ». Qui suis-je ?",
                "choices": ["La lettre N", "La lettre A", "La lettre U", "La lettre I"],
                "answer": "La lettre N",
            },
            {
                "riddle": "Un berger possède dix-sept moutons. Tous meurent, sauf neuf. Combien lui en reste-t-il ?",
                "choices": ["Neuf", "Huit", "Dix-sept", "Aucun"],
                "answer": "Neuf",
            },
        ],
    ]

    def tirer_enigme(niv):
        """Tire une énigme du niveau donné et renvoie (énigme, réponses mélangées)."""
        enigme = renpy.random.choice(enigmes_par_niveau[niv])
        choix = list(enigme["choices"])
        renpy.random.shuffle(choix)
        return enigme, choix

    def fond_porte(porte):
        """Fond dédié de la porte s'il existe, sinon le fond de secours."""
        if renpy.has_image(porte["bg"]):
            return porte["bg"]
        return porte["bg_secours"]
