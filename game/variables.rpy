########################################
# LE MANOIR-LABYRINTHE — variables.rpy
# Variables globales et données des énigmes
########################################

# Règles :
# - le joueur commence avec 1 fragment et en mise un à chaque porte ;
# - bonne réponse : il le récupère et en gagne un ; mauvaise : il le perd ;
# - victoire dès qu'il réunit 4 fragments ;
# - défaite s'il n'a plus de fragment à miser, ou après 10 manches.
# La difficulté suit le nombre de fragments possédés : 1 -> niveau 0
# (très simple), 2 -> niveau 1, 3 -> niveau 2 (la porte qui ferait gagner).
define total_pieces = 4           # fragments nécessaires pour reconstituer la carte
define max_manches = 10           # nombre maximum de portes

default pieces_owned = []         # liste des pièces possédées, ex: ["piece_01", "piece_02"]
default manche = 0                # numéro de la porte en cours (1 à max_manches)
default niveau = 0                # difficulté de la porte en cours (0, 1, 2)
default enigme_courante = None    # énigme tirée pour la porte en cours
default choix_melanges = []       # réponses de l'énigme, dans un ordre aléatoire
default enigmes_vues = []         # énigmes déjà posées, pour éviter les répétitions

init python:

    # Une porte par niveau : décor et textes d'arrivée (un est tiré au hasard).
    # "bg" est le fond dédié ; "bg_secours" sert tant qu'il n'existe pas.
    portes = [
        {
            "bg": "bg_door_level_0",
            "bg_secours": "bg_corridor_01",
            "intros": [
                "Au bout du couloir, une porte de chêne toute simple vous attend, éclairée par une bougie posée sur un guéridon. Une voix douce, presque amusée, murmure à travers le bois.",
                "La porte de chêne est revenue, comme si le couloir avait tourné sur lui-même. La bougie brûle toujours, et la voix semble presque indulgente.",
                "Une porte claire, presque accueillante, se dresse devant vous. Ici, le manoir paraît vouloir vous laisser une chance.",
            ],
        },
        {
            "bg": "bg_door_level_1",
            "bg_secours": "bg_library",
            "intros": [
                "Une porte se cache au fond de la bibliothèque, ses panneaux couverts de lettres gravées. L'air sent le vieux papier, et la voix, cette fois, ne sourit plus.",
                "Entre deux rayonnages, la porte gravée vous attend. Les livres semblent s'être rapprochés pour mieux écouter votre réponse.",
                "La bibliothèque est plus sombre qu'avant. Sur la porte, les lettres gravées remuent à peine, comme si elles respiraient.",
            ],
        },
        {
            "bg": "bg_door_level_2",
            "bg_secours": "bg_secret_room",
            "intros": [
                "Une porte noire, immense, striée de runes dorées qui pulsent comme un cœur. Derrière elle, vous le sentez, il y a la sortie. La voix gronde, grave et patiente.",
                "La grande porte noire se dresse de nouveau. Les runes battent plus vite à votre approche : un seul morceau de plus, et la carte serait complète.",
                "La brume rampe au pied de la porte aux runes d'or. La voix ne murmure plus : elle attend, et elle sait que vous êtes tout près.",
            ],
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
            {
                "riddle": "Je suis jaune, je brille dans le ciel pendant la journée et je réchauffe la terre. Qui suis-je ?",
                "choices": ["Le soleil", "La lune", "Un nuage", "La pluie"],
                "answer": "Le soleil",
            },
            {
                "riddle": "J'ai des ailes, des plumes et un bec, et je chante le matin. Qui suis-je ?",
                "choices": ["Un oiseau", "Un chat", "Un poisson", "Un serpent"],
                "answer": "Un oiseau",
            },
            {
                "riddle": "On m'allume quand il fait noir, et je fonds doucement en brûlant. Qui suis-je ?",
                "choices": ["Une bougie", "Une lampe", "Un miroir", "Une clé"],
                "answer": "Une bougie",
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
            {
                "riddle": "J'ai une tête et une queue, mais pas de corps. Qui suis-je ?",
                "choices": ["Une pièce de monnaie", "Un serpent", "Un poisson", "Un oiseau"],
                "answer": "Une pièce de monnaie",
            },
            {
                "riddle": "Plus il y en a, moins on y voit. Qu'est-ce que c'est ?",
                "choices": ["L'obscurité", "La lumière", "Le silence", "Le bruit"],
                "answer": "L'obscurité",
            },
            {
                "riddle": "Je suis toujours devant toi, mais tu ne me verras jamais. Qui suis-je ?",
                "choices": ["L'avenir", "Le passé", "Ton reflet", "Le ciel"],
                "answer": "L'avenir",
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
            {
                "riddle": "Devant un portrait, un homme déclare : « Je n'ai ni frère ni sœur, mais le père de cet homme est le fils de mon père. » Qui est sur le portrait ?",
                "choices": ["Son fils", "Lui-même", "Son père", "Son neveu"],
                "answer": "Son fils",
            },
            {
                "riddle": "J'ai des aiguilles mais je ne pique pas. Je n'ai pas de jambes, et pourtant je cours sans jamais m'arrêter. Qui suis-je ?",
                "choices": ["Une horloge", "Un hérisson", "Un sapin", "Une couturière"],
                "answer": "Une horloge",
            },
            {
                "riddle": "Plus puissant que Dieu, plus méchant que le diable. Les pauvres en ont, les riches en manquent, et celui qui en mange meurt. Qu'est-ce que c'est ?",
                "choices": ["Rien", "Le temps", "L'argent", "La mort"],
                "answer": "Rien",
            },
        ],
    ]

    def tirer_enigme(niv, deja_vues):
        """Tire une énigme du niveau donné, pas encore posée si possible,
        et renvoie (énigme, réponses mélangées)."""
        pool = [e for e in enigmes_par_niveau[niv] if e["riddle"] not in deja_vues]
        enigme = renpy.random.choice(pool or enigmes_par_niveau[niv])
        choix = list(enigme["choices"])
        renpy.random.shuffle(choix)
        return enigme, choix

    def prochaine_piece(possedees):
        """Premier fragment de la carte que le joueur ne possède pas."""
        for n in range(1, total_pieces + 1):
            pid = "piece_%02d" % n
            if pid not in possedees:
                return pid

    def fond_porte(porte):
        """Fond dédié de la porte s'il existe, sinon le fond de secours."""
        if renpy.has_image(porte["bg"]):
            return porte["bg"]
        return porte["bg_secours"]
