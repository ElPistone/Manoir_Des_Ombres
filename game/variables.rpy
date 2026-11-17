########################################
# LE MANOIR DES OMBRES — variables.rpy
# Règles, fragments, énigmes et fonctions utilitaires
########################################

# Règles :
# - le joueur commence avec 1 fragment et en mise un à chaque porte ;
# - bonne réponse : il le récupère et en gagne un ; mauvaise : il le perd ;
# - chaque fragment possédé donne un POUVOIR, mais le fragment misé est sous
#   la porte : son pouvoir ne joue pas pour cette énigme ;
# - avec 2 fragments, on peut tout risquer (double mise) : énigme plus dure,
#   mais 2 fragments gagnés d'un coup ;
# - à chaque salle, deux portes : la porte de chêne (énigme à choix) ou la
#   porte qui murmure (fouille de la salle ou réponse à taper), qui rallume
#   la bougie et livre une page du journal d'Éléonore si l'on répond juste ;
# - la BOUGIE remplace le compteur de portes : elle éclaire 12 portes, perd
#   une porte quand on implore un indice, en regagne une à la porte qui murmure ;
# - une fois la carte complète (4 fragments), il reste la PORTE DE SORTIE :
#   deux énigmes à réponse libre ; une erreur coûte encore un fragment ;
# - défaite s'il n'a plus de fragment à miser, ou si la bougie s'éteint.
# La difficulté suit le nombre de fragments possédés :
# 1 -> niveau 0, 2 -> niveau 1, 3 -> niveau 2, 4 -> niveau 3 (sortie).
define total_pieces = 4           # fragments nécessaires pour reconstituer la carte
define max_manches = 12           # portes que la bougie peut éclairer au départ
define etapes_sortie = 2          # la porte de sortie a deux verrous
define niveau_sortie = 3          # niveau de l'énigme de la porte de sortie

default pieces_owned = []         # fragments possédés, ex: ["piece_01", "piece_03"]
default manche = 0                # numéro de la porte en cours (1 à max_manches)
default niveau = 0                # difficulté de la porte en cours (0 à 3)
default enigme_courante = None    # énigme tirée pour la porte en cours
default choix_melanges = []       # réponses de l'énigme, dans un ordre aléatoire
default enigmes_vues = []         # énigmes déjà posées, pour éviter les répétitions
default mise = []                 # fragment(s) misé(s) à la porte en cours
default erreurs = 0               # nombre de mauvaises réponses dans la partie
default cle_utilisee = False      # le pouvoir de la Clé ne sert qu'une fois par partie
default id_partie = ""            # identifiant de la partie (anti-triche)
default bonus_bougie = 0          # portes gagnées (porte qui murmure) ou perdues (indice imploré)
default porte_murmure = False     # le joueur a choisi la porte qui murmure
default salle_courante = "bg_entrance_hall"  # pièce où se trouve la porte en cours
default carte_complete_vue = False  # la carte a été complète au moins une fois dans la partie
default serie_ok = 0              # bonnes réponses d'affilée
default serie_ko = 0              # erreurs d'affilée

# Mémoire du manoir : le verdict de chaque porte déjà répondue. Recharger une
# sauvegarde faite devant une énigme ne permet donc pas de changer de réponse.
default persistent.verdicts = {}
# Fins découvertes (écran titre et écran « Secrets du manoir »)
default persistent.fins_vues = set()
# Mémoire entre les parties : le manoir se souvient de ses visiteurs
default persistent.parties = 0
default persistent.derniere_fin = None
# Pages du journal d'Éléonore retrouvées (gardées d'une partie à l'autre)
default persistent.pages_journal = set()
# Accessibilité
default persistent.texte_grand = False
default persistent.sans_flash = False

init python:
    import re
    import unicodedata

    # ------------------------------------------------------------------
    # LES FRAGMENTS ET LEURS POUVOIRS
    # ------------------------------------------------------------------
    # Le dos de chaque fragment porte une note : on découvre l'histoire du
    # manoir en reconstituant la carte.
    fragments = {
        "piece_01": {
            "nom": "Fragment de la Lanterne",
            "pouvoir": "Lanterne",
            "effet": "La voix vous souffle un indice.",
            "lore": "« Plan du manoir Blackwood, relevé de ma main à l'automne 1847. Que nul ne s'y perde jamais. — Edmund Blackwood »",
        },
        "piece_02": {
            "nom": "Fragment de l'Encre",
            "pouvoir": "Encre",
            "effet": "Une mauvaise réponse est barrée (ou la première lettre révélée).",
            "lore": "« Éléonore pose trop de questions sur le monde du dehors. J'ai fait murer les portes du nord. Elle ne partira pas comme sa mère. »",
        },
        "piece_03": {
            "nom": "Fragment du Sablier",
            "pouvoir": "Sablier",
            "effet": "Une fois par porte, vous pouvez demander une autre énigme.",
            "lore": "« Père a déchiré la carte en quatre et l'a cachée dans les murs. Le soir, quand je cherche la sortie, j'entends les couloirs bouger. — É. »",
        },
        "piece_04": {
            "nom": "Fragment de la Clé",
            "pouvoir": "Clé",
            "effet": "Une fois par partie, une erreur ne vous coûte rien.",
            "lore": "« Si quelqu'un lit ceci, rassemblez les morceaux et sortez. Et, je vous en supplie, emmenez-moi avec vous. — Éléonore »",
        },
    }

    def pouvoirs_actifs(possedees, misees):
        """Pouvoirs des fragments possédés, sauf ceux glissés sous la porte."""
        return [fragments[p]["pouvoir"] for p in possedees if p not in misees]

    def prochaine_piece(possedees):
        """Un fragment manquant, tiré au hasard : on ne sait jamais quel
        pouvoir on va obtenir."""
        manquantes = ["piece_%02d" % n for n in range(1, total_pieces + 1)
                      if "piece_%02d" % n not in possedees]
        return renpy.random.choice(manquantes) if manquantes else None

    # ------------------------------------------------------------------
    # LES PORTES (une par niveau)
    # ------------------------------------------------------------------
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
                "Une porte noire, immense, striée de runes dorées qui pulsent comme un cœur. Derrière elle, vous le sentez, la carte attend son dernier morceau. La voix gronde, grave et patiente.",
                "La grande porte noire se dresse de nouveau. Les runes battent plus vite à votre approche : un seul morceau de plus, et la carte serait complète.",
                "La brume rampe au pied de la porte aux runes d'or. La voix ne murmure plus : elle attend, et elle sait que vous êtes tout près.",
            ],
        },
        {
            "bg": "bg_door_generic",
            "bg_secours": "bg_secret_room",
            "intros": [
                "La carte complète vous guide jusqu'à une porte basse, couverte de signes, que vous n'aviez jamais vue. De l'autre côté, vous jureriez sentir l'air froid du dehors.",
                "La porte de sortie est là, exactement où la carte l'indique. La voix tremble : « Cette fois, aucune réponse ne te sera proposée. Trouve-la seul. »",
            ],
        },
    ]

    def fond_porte(porte):
        """Fond dédié de la porte s'il existe, sinon le fond de secours."""
        if renpy.has_image(porte["bg"]):
            return porte["bg"]
        return porte["bg_secours"]

    # ------------------------------------------------------------------
    # LES ÉNIGMES
    # ------------------------------------------------------------------
    # Chaque énigme a un "indice" (pouvoir de la Lanterne). Les réponses à
    # choix sont mélangées : "answer" est donc le TEXTE de la bonne réponse.
    # "illus" (facultatif) affiche une illustration à côté de l'énigme.
    # Les énigmes "saisie" se répondent au clavier : "accepte" liste les
    # réponses admises (comparées sans accents, articles ni majuscules).
    enigmes_par_niveau = [
        # --- Niveau 0 : volontairement très simple (une erreur fait perdre) ---
        [
            {"riddle": "Je suis blanche, je tombe du ciel en hiver et je fonds au soleil. Qui suis-je ?",
             "choices": ["La neige", "La pluie", "Le sable", "La cendre"], "answer": "La neige",
             "indice": "Les enfants en font des bonshommes."},
            {"riddle": "Je brille dans le ciel la nuit, et ma forme change au fil du mois. Qui suis-je ?",
             "choices": ["La lune", "Le soleil", "Un nuage", "Un oiseau"], "answer": "La lune",
             "indice": "On dit qu'elle est pleine, ou nouvelle."},
            {"riddle": "Je porte le nom de ma propre couleur, et l'on me mange en hiver. Quel fruit suis-je ?",
             "choices": ["L'orange", "La pomme", "La poire", "La fraise"], "answer": "L'orange",
             "indice": "Je suis un agrume."},
            {"riddle": "On me monte et on me descend, mais je ne bouge jamais. Qui suis-je ?",
             "choices": ["Un escalier", "Un ascenseur", "Un ballon", "Un cheval"], "answer": "Un escalier",
             "indice": "Le hall du manoir en a un très grand."},
            {"riddle": "Je suis jaune, je brille dans le ciel pendant la journée et je réchauffe la terre. Qui suis-je ?",
             "choices": ["Le soleil", "La lune", "Un nuage", "La pluie"], "answer": "Le soleil",
             "indice": "Je me lève à l'est."},
            {"riddle": "J'ai des ailes, des plumes et un bec, et je chante le matin. Qui suis-je ?",
             "choices": ["Un oiseau", "Un chat", "Un poisson", "Un serpent"], "answer": "Un oiseau",
             "indice": "Je fais mon nid dans les arbres."},
            {"riddle": "On m'allume quand il fait noir, et je fonds doucement en brûlant. Qui suis-je ?",
             "choices": ["Une bougie", "Une lampe", "Un miroir", "Une clé"], "answer": "Une bougie",
             "indice": "Je suis faite de cire."},
            {"riddle": "Je pousse sur les branches au printemps et je tombe en automne. Qui suis-je ?",
             "choices": ["Une feuille", "Une pierre", "Un nid", "Une racine"], "answer": "Une feuille",
             "indice": "Je suis verte, puis rousse."},
            {"riddle": "Il faut me casser avant de pouvoir me manger. Qui suis-je ?",
             "choices": ["Un œuf", "Un gâteau", "Une soupe", "Une banane"], "answer": "Un œuf",
             "indice": "La poule y est pour quelque chose."},
            {"riddle": "J'ai un pied et un chapeau, et je pousse dans la forêt après la pluie. Qui suis-je ?",
             "choices": ["Un champignon", "Un sapin", "Un écureuil", "Un rocher"], "answer": "Un champignon",
             "indice": "Certains sont comestibles, d'autres mortels."},
            {"riddle": "Plus je travaille, plus je raccourcis. Je sers à écrire et à dessiner. Qui suis-je ?",
             "choices": ["Un crayon", "Un livre", "Une règle", "Une gomme"], "answer": "Un crayon",
             "indice": "On me taille."},
            {"riddle": "Je garde la maison, j'aboie quand on frappe et je remue la queue. Qui suis-je ?",
             "choices": ["Un chien", "Un chat", "Un hibou", "Un cheval"], "answer": "Un chien",
             "indice": "Je suis le meilleur ami de l'homme."},
            {"riddle": "Dans le grenier, je tisse ma toile dans tous les coins, et j'ai huit pattes. Qui suis-je ?",
             "choices": ["Une araignée", "Une fourmi", "Un papillon", "Une souris"], "answer": "Une araignée",
             "indice": "Regardez les toiles accrochées aux poutres.", "salle": "bg_attic"},
        ],
        # --- Niveau 1 : il faut réfléchir ---
        [
            {"riddle": "Plus on m'enlève de matière, plus je deviens grand. Qui suis-je ?",
             "choices": ["Un trou", "Un mur", "Un arbre", "Une montagne"], "answer": "Un trou",
             "indice": "Prenez une pelle et creusez."},
            {"riddle": "Je suis plein de trous, et pourtant je retiens l'eau. Qui suis-je ?",
             "choices": ["Une éponge", "Un seau", "Un filet", "Une passoire"], "answer": "Une éponge",
             "indice": "On me presse pour me vider."},
            {"riddle": "Plus je sèche, plus je suis mouillée. Qui suis-je ?",
             "choices": ["Une serviette", "Une éponge", "Un miroir", "Un livre"], "answer": "Une serviette",
             "indice": "On s'en sert en sortant du bain."},
            {"riddle": "Il est à vous, mais les autres s'en servent bien plus que vous. Qu'est-ce que c'est ?",
             "choices": ["Votre prénom", "Votre maison", "Votre ombre", "Votre voix"], "answer": "Votre prénom",
             "indice": "On vous appelle par lui."},
            {"riddle": "J'ai une tête et une queue, mais pas de corps. Qui suis-je ?",
             "choices": ["Une pièce de monnaie", "Un serpent", "Un poisson", "Un oiseau"], "answer": "Une pièce de monnaie",
             "indice": "Pile ou face ?"},
            {"riddle": "Plus il y en a, moins on y voit. Qu'est-ce que c'est ?",
             "choices": ["L'obscurité", "La lumière", "Le silence", "Le bruit"], "answer": "L'obscurité",
             "indice": "Ce manoir en est rempli."},
            {"riddle": "Je suis toujours devant toi, mais tu ne me verras jamais. Qui suis-je ?",
             "choices": ["L'avenir", "Le passé", "Ton reflet", "Le ciel"], "answer": "L'avenir",
             "indice": "Demain en fait partie."},
            {"riddle": "J'ai des touches noires et blanches, mais je ne sais pas écrire. Qui suis-je ?",
             "choices": ["Un piano", "Une machine à écrire", "Un zèbre", "Un échiquier"], "answer": "Un piano",
             "indice": "On joue sur moi."},
            {"riddle": "Le matin, je marche à quatre pattes ; à midi, sur deux ; le soir, sur trois. Qui suis-je ?",
             "choices": ["L'homme", "Le chat", "Le cheval", "L'araignée"], "answer": "L'homme",
             "indice": "Le matin, le midi et le soir sont les âges de la vie."},
            {"riddle": "Je monte sans cesse, mais je ne redescends jamais. Qui suis-je ?",
             "choices": ["L'âge", "Un ascenseur", "Un ballon", "La marée"], "answer": "L'âge",
             "indice": "On le fête chaque année."},
            {"riddle": "J'ai des dents, mais je ne mords jamais. Qui suis-je ?",
             "choices": ["Un peigne", "Un chien", "Un requin", "Un serpent"], "answer": "Un peigne",
             "indice": "Je passe dans les cheveux."},
            {"riddle": "Je cours sans jambes, j'ai un lit mais je ne dors jamais. Qui suis-je ?",
             "choices": ["Une rivière", "Le vent", "Un nuage", "Une horloge"], "answer": "Une rivière",
             "indice": "Je finis dans la mer."},
            {"riddle": "Plus je vieillis au fond de cette cave, plus on me trouve bon. Qui suis-je ?",
             "choices": ["Le vin", "Le pain", "Le lait", "La soupe"], "answer": "Le vin",
             "indice": "On me garde dans un tonneau.", "salle": "bg_cellar"},
            {"riddle": "On me couvre d'un drap pour me protéger, et pourtant je n'ai jamais froid. Je reçois tout le monde sans jamais me lever. Qui suis-je ?",
             "choices": ["Un fauteuil", "Un fantôme", "Un lit", "Un chat"], "answer": "Un fauteuil",
             "indice": "Les meubles du grenier dorment sous des draps.", "salle": "bg_attic"},
            {"riddle": "Dans ce couloir, le premier tableau est accroché à 1 mètre de la porte, puis il y en a un tous les 2 mètres. À quelle distance de la porte se trouve le cinquième ?",
             "choices": ["9 m", "10 m", "11 m", "8 m"], "answer": "9 m",
             "indice": "Entre le premier et le cinquième, il n'y a que quatre intervalles.", "salle": "bg_corridor_01",
             "accepte": ["9", "9 m", "9 metres", "neuf", "neuf metres"]},
        ],
        # --- Niveau 2 : vraiment difficile, souvent un piège ---
        [
            {"riddle": "Celui qui me fabrique me vend. Celui qui m'achète ne se sert pas de moi. Celui qui se sert de moi ne me voit jamais. Qui suis-je ?",
             "choices": ["Un cercueil", "Un cadeau", "Une perruque", "Un miroir"], "answer": "Un cercueil",
             "indice": "Celui qui s'en sert ne voit plus rien du tout."},
            {"riddle": "Le père d'Éléonore a cinq filles : Lala, Lélé, Lili et Lolo. Comment s'appelle la cinquième ?",
             "choices": ["Éléonore", "Lulu", "Lyly", "Lala"], "answer": "Éléonore",
             "indice": "Relisez le début de la question."},
            {"riddle": "On me trouve deux fois dans « année », une fois dans « nuit », et jamais dans « jour ». Qui suis-je ?",
             "choices": ["La lettre N", "La lettre A", "La lettre U", "La lettre I"], "answer": "La lettre N",
             "indice": "Regardez les lettres, pas le sens des mots."},
            {"riddle": "Un berger possède dix-sept moutons. Tous meurent, sauf neuf. Combien lui en reste-t-il ?",
             "choices": ["Neuf", "Huit", "Dix-sept", "Aucun"], "answer": "Neuf",
             "indice": "Il n'y a aucun calcul à faire."},
            {"riddle": "Devant ce portrait, la maîtresse des lieux murmure : « Je n'ai ni frère ni sœur, mais la mère de cette femme est la fille de ma mère. » Qui est sur le portrait ?",
             "choices": ["Sa fille", "Elle-même", "Sa mère", "Sa nièce"], "answer": "Sa fille",
             "indice": "Fille unique, la fille de sa mère, c'est elle.", "illus": "portrait"},
            {"riddle": "J'ai des aiguilles mais je ne pique pas. Je n'ai pas de jambes, et pourtant je cours sans jamais m'arrêter. Qui suis-je ?",
             "choices": ["Une horloge", "Un hérisson", "Un sapin", "Une couturière"], "answer": "Une horloge",
             "indice": "Le temps file avec moi."},
            {"riddle": "Plus puissant que Dieu, plus méchant que le diable. Les pauvres en ont, les riches en manquent, et celui qui en mange meurt. Qu'est-ce que c'est ?",
             "choices": ["Rien", "Le temps", "L'argent", "La mort"], "answer": "Rien",
             "indice": "Prenez chaque phrase au pied de la lettre."},
            {"riddle": "L'horloge du grand hall a deux aiguilles. Combien de fois se superposent-elles en douze heures ?",
             "choices": ["Onze", "Douze", "Vingt-quatre", "Six"], "answer": "Onze",
             "indice": "Entre 11 h et 13 h, elles ne se rejoignent qu'une seule fois : à midi.", "illus": "clock"},
            {"riddle": "Ce cadenas s'ouvre avec trois chiffres tous différents. Leur somme fait 6, leur produit aussi. Le code est le plus grand nombre possible. Quel est-il ?",
             "choices": ["321", "123", "312", "222"], "answer": "321",
             "indice": "Trouvez les trois chiffres, puis rangez-les du plus grand au plus petit.", "illus": "lock"},
            {"riddle": "Deux tomes de 100 pages sont rangés dans l'ordre sur l'étagère, dos face à vous. Un ver ronge de la première page du tome I jusqu'à la dernière page du tome II. Combien de pages traverse-t-il, couvertures non comptées ?",
             "choices": ["Aucune", "200", "100", "2"], "answer": "Aucune",
             "indice": "Sur une étagère, où se trouve la première page d'un livre dont le dos vous fait face ?", "illus": "book"},
            {"riddle": "Dans le miroir fêlé de la chambre, une horloge sans chiffres semble indiquer 3 h pile. Quelle heure est-il vraiment ?",
             "choices": ["9 h", "3 h", "6 h", "12 h"], "answer": "9 h",
             "indice": "Un miroir inverse la gauche et la droite.", "illus": "mirror"},
            {"riddle": "Un homme monte cet escalier de 12 marches deux par deux, puis le redescend trois par trois. Combien de pas a-t-il faits en tout ?",
             "choices": ["10", "12", "24", "5"], "answer": "10",
             "indice": "Comptez la montée, puis la descente, séparément.", "salle": "bg_stairs",
             "accepte": ["10", "dix"]},
        ],
        # --- Niveau 3 : la porte de sortie, réponse libre au clavier ---
        [
            {"saisie": True,
             "riddle": "J'ai des villes sans maisons, des forêts sans arbres et des rivières sans eau. Qui suis-je ?",
             "answer": "Une carte", "accepte": ["carte", "plan"],
             "indice": "Vous en tenez justement les morceaux."},
            {"saisie": True,
             "riddle": "Je te suis quand vient le jour, je te quitte quand vient la nuit. Qui suis-je ?",
             "answer": "Ton ombre", "accepte": ["ombre"],
             "indice": "Ce manoir porte mon nom."},
            {"saisie": True,
             "riddle": "Je parle sans bouche et j'entends sans oreilles. Je n'ai pas de corps, mais je réponds à qui m'appelle. Qui suis-je ?",
             "answer": "L'écho", "accepte": ["echo"],
             "indice": "Criez dans une grotte."},
            {"saisie": True,
             "riddle": "Il suffit de prononcer mon nom pour me briser. Qui suis-je ?",
             "answer": "Le silence", "accepte": ["silence"],
             "indice": "Chut…"},
            {"saisie": True,
             "riddle": "Plus j'ai de gardiens, moins je suis gardé. Qui suis-je ?",
             "answer": "Un secret", "accepte": ["secret"],
             "indice": "Ne le répétez à personne."},
            {"saisie": True,
             "riddle": "Je suis au début de l'éternité, à la fin de la vie et au milieu de la mer. Qui suis-je ?",
             "answer": "La lettre E", "accepte": ["e", "lettre e"],
             "indice": "Regardez les mots eux-mêmes, lettre par lettre."},
        ],
    ]

    # Compléments : salle où l'énigme se pose de préférence, et réponses
    # admises au clavier (porte qui murmure). Sans "accepte", une réponse
    # d'un seul mot est acceptée telle quelle (sans article ni accent).
    complements = {
        "Un escalier": {"salle": "bg_stairs"},
        "Une bougie": {"salle": "bg_cellar"},
        "Onze": {"salle": "bg_entrance_hall", "accepte": ["onze", "11"]},
        "9 h": {"salle": "bg_corridor_02", "accepte": ["9", "9 h", "neuf", "neuf heures", "9 heures"]},
        "Sa fille": {"salle": "bg_corridor_01"},
        "Une pièce de monnaie": {"accepte": ["piece", "piece monnaie", "monnaie"]},
        "La lettre N": {"accepte": ["n", "lettre n"]},
        "L'obscurité": {"accepte": ["obscurite", "noir", "nuit", "tenebres"]},
        "L'avenir": {"accepte": ["avenir", "futur"]},
        "L'homme": {"accepte": ["homme", "humain", "etre humain"]},
        "Aucune": {"accepte": ["aucune", "aucun", "zero", "0"]},
        "Neuf": {"accepte": ["neuf", "9"]},
        "Une rivière": {"accepte": ["riviere", "fleuve"]},
        "Votre prénom": {"accepte": ["prenom", "nom"]},
    }

    # ------------------------------------------------------------------
    # LES FOUILLES : énigmes visuelles, on clique sur l'objet dans la salle
    # ------------------------------------------------------------------
    # "zones" : rectangles (x0, y0, x1, y1) en fractions de l'écran.
    fouilles = [
        {"salle": "bg_entrance_hall", "answer": "lustre", "indice": "Levez les yeux.",
         "riddle": "Je porte des flammes sans jamais brûler, je pends au-dessus de vos têtes et je n'ai jamais touché le sol. Montrez-moi.",
         "zones": {"lustre": (0.41, 0.08, 0.58, 0.27), "escalier": (0.34, 0.44, 0.66, 0.79),
                   "porte de gauche": (0.08, 0.16, 0.20, 0.82), "porte de droite": (0.80, 0.16, 0.93, 0.82),
                   "tapis": (0.34, 0.82, 0.66, 0.99)}},
        {"salle": "bg_entrance_hall", "answer": "tapis", "indice": "Il couvre les marches et le sol.",
         "riddle": "Je suis un long chemin rouge que tout le monde piétine, et personne ne s'en excuse. Montrez-moi.",
         "zones": {"lustre": (0.41, 0.08, 0.58, 0.27), "tapis": (0.34, 0.82, 0.66, 0.99),
                   "porte de gauche": (0.08, 0.16, 0.20, 0.82), "porte de droite": (0.80, 0.16, 0.93, 0.82)}},
        {"salle": "bg_attic", "answer": "fauteuil à bascule", "indice": "Il attend dans l'ombre, au fond à droite.",
         "riddle": "Je me balance sans vent, et pourtant personne ne s'assoit sur moi. Montrez-moi.",
         "zones": {"fauteuil à bascule": (0.79, 0.52, 0.88, 0.75), "miroir": (0.60, 0.46, 0.70, 0.79),
                   "lucarne": (0.53, 0.30, 0.61, 0.42), "malles": (0.40, 0.60, 0.60, 0.86),
                   "canapé couvert": (0.18, 0.57, 0.40, 0.85)}},
        {"salle": "bg_attic", "answer": "lucarne", "indice": "La lumière bleue entre par là.",
         "riddle": "Je suis un œil rond dans le mur, et la lune regarde à travers moi. Montrez-moi.",
         "zones": {"fauteuil à bascule": (0.79, 0.52, 0.88, 0.75), "miroir": (0.60, 0.46, 0.70, 0.79),
                   "lucarne": (0.53, 0.30, 0.61, 0.42), "malles": (0.40, 0.60, 0.60, 0.86)}},
        {"salle": "bg_cellar", "answer": "tonneau", "indice": "La bougie est posée sur lui.",
         "riddle": "J'ai un ventre rond et je garde le vin, mais je n'ai jamais soif. Montrez-moi.",
         "zones": {"tonneau": (0.22, 0.58, 0.38, 0.88), "bougie": (0.27, 0.42, 0.33, 0.56),
                   "caisses": (0.77, 0.43, 0.90, 0.67), "flaque": (0.42, 0.76, 0.70, 0.96),
                   "tunnel": (0.52, 0.27, 0.78, 0.55)}},
        {"salle": "bg_cellar", "answer": "bougie", "indice": "Je suis la seule lumière de la cave.",
         "riddle": "Je pleure de la cire et je meurs en vous éclairant. Montrez-moi.",
         "zones": {"tonneau": (0.22, 0.58, 0.38, 0.88), "bougie": (0.27, 0.42, 0.33, 0.56),
                   "caisses": (0.77, 0.43, 0.90, 0.67), "tunnel": (0.52, 0.27, 0.78, 0.55)}},
        {"salle": "bg_stairs", "answer": "lanterne", "indice": "Elle pend à un bras de fer forgé.",
         "riddle": "Je suis une prison de verre pour une petite flamme. Montrez-moi.",
         "zones": {"lanterne": (0.30, 0.40, 0.43, 0.54), "marches du haut": (0.53, 0.06, 0.86, 0.34),
                   "marches du bas": (0.53, 0.60, 0.86, 0.90), "colonne": (0.46, 0.06, 0.53, 0.95)}},
        {"salle": "bg_stairs", "answer": "colonne", "indice": "Je suis au centre de l'escalier.",
         "riddle": "Tous les pas tournent autour de moi, et je n'en fais jamais un seul. Montrez-moi.",
         "zones": {"lanterne": (0.30, 0.40, 0.43, 0.54), "marches du haut": (0.55, 0.06, 0.86, 0.34),
                   "marches du bas": (0.55, 0.60, 0.86, 0.90), "colonne": (0.46, 0.06, 0.54, 0.95)}},
        {"salle": "bg_corridor_02", "answer": "miroir", "indice": "Ma surface est fêlée de partout.",
         "riddle": "Je suis brisé, et pourtant je vous montre encore une autre pièce. Montrez-moi.",
         "zones": {"miroir": (0.17, 0.10, 0.40, 0.70), "applique": (0.65, 0.37, 0.71, 0.48),
                   "tapis": (0.45, 0.86, 0.76, 0.99), "voûte": (0.60, 0.01, 0.85, 0.30)}},
        {"salle": "bg_corridor_02", "answer": "applique", "indice": "Une seule flamme brûle dans ce couloir.",
         "riddle": "Je suis une petite main de métal qui tient la lumière contre le mur. Montrez-moi.",
         "zones": {"miroir": (0.17, 0.10, 0.40, 0.70), "applique": (0.65, 0.37, 0.71, 0.48),
                   "tapis": (0.45, 0.86, 0.76, 0.99), "voûte": (0.60, 0.01, 0.85, 0.30)}},
        {"salle": "bg_corridor_01", "answer": "tableaux", "indice": "Ils sont accrochés aux murs, dans des cadres dorés.",
         "riddle": "Nous vous regardons passer depuis des années, mais nous n'avons jamais cligné des yeux. Montrez-nous.",
         "zones": {"tableaux": (0.73, 0.08, 0.84, 0.57), "applique": (0.20, 0.22, 0.27, 0.40),
                   "porte du fond": (0.46, 0.41, 0.56, 0.62), "tapis": (0.32, 0.72, 0.68, 0.99)}},
        {"salle": "bg_corridor_01", "answer": "porte du fond", "indice": "Regardez tout au bout du couloir.",
         "riddle": "Je suis au bout de tout, et plus vous marchez vers moi, moins je semble approcher. Montrez-moi.",
         "zones": {"tableaux": (0.73, 0.08, 0.84, 0.57), "applique": (0.20, 0.22, 0.27, 0.40),
                   "porte du fond": (0.46, 0.41, 0.56, 0.62), "tapis": (0.32, 0.72, 0.68, 0.99)}},
    ]
    for _f in fouilles:
        _f["fouille"] = True

    def reponses_admises(enigme):
        """Réponses acceptées au clavier, ou [] si l'énigme ne s'y prête pas."""
        if "accepte" in enigme:
            return enigme["accepte"]
        mot = normaliser(enigme.get("answer", ""))
        return [mot] if mot and " " not in mot else []

    for _niv in enigmes_par_niveau:
        for _e in _niv:
            _e.update(complements.get(_e.get("answer"), {}))

    def tirer_enigme(niv, deja_vues, sauf=None, salle=None, saisie=False):
        """Tire une énigme du niveau donné, pas encore posée si possible
        (et différente de « sauf »), de préférence liée à la salle, et renvoie
        (énigme, réponses mélangées). Avec saisie=True, l'énigme se répond
        au clavier."""
        toutes = enigmes_par_niveau[niv]
        if saisie:
            toutes = [e for e in toutes if reponses_admises(e)] or toutes
        sauf_txt = sauf["riddle"] if sauf else None
        pool = [e for e in toutes if e["riddle"] not in deja_vues and e["riddle"] != sauf_txt]
        if not pool:
            pool = [e for e in toutes if e["riddle"] != sauf_txt] or toutes
        de_la_salle = [e for e in pool if salle and e.get("salle") == salle]
        enigme = renpy.random.choice(de_la_salle or pool)
        if saisie and not enigme.get("saisie"):
            enigme = dict(enigme, saisie=True, accepte=reponses_admises(enigme))
        choix = [] if enigme.get("saisie") else list(enigme.get("choices", []))
        renpy.random.shuffle(choix)
        return enigme, choix

    def tirer_fouille(salle, deja_vues, sauf=None):
        """Une fouille de la salle pas encore posée, ou None."""
        pool = [f for f in fouilles if f["salle"] == salle and f["riddle"] not in deja_vues
                and (sauf is None or f["riddle"] != sauf.get("riddle"))]
        return renpy.random.choice(pool) if pool else None

    def tirer_murmure(niv, deja_vues, salle, sauf=None):
        """Énigme de la porte qui murmure : une fouille de la salle si
        possible, sinon une énigme à réponse libre."""
        f = tirer_fouille(salle, deja_vues, sauf)
        if f is not None and renpy.has_image(salle):
            return f, []
        return tirer_enigme(niv, deja_vues, sauf=sauf, salle=salle, saisie=True)

    def reponse_barree(enigme, choix):
        """Pouvoir de l'Encre : une mauvaise réponse (ou zone) à barrer."""
        if enigme.get("fouille"):
            choix = list(enigme["zones"].keys())
        fausses = [c for c in choix if c != enigme["answer"]]
        return renpy.random.choice(fausses) if fausses else None

    MOTS_VIDES = {"le", "la", "les", "l", "un", "une", "des", "du", "de", "d",
                  "ton", "ta", "tes", "mon", "ma", "mes", "votre", "vos",
                  "son", "sa", "ses", "c", "est", "s", "il", "elle"}

    def normaliser(texte):
        """Minuscules, sans accents, sans ponctuation ni articles."""
        texte = texte.lower().replace("œ", "oe").replace("æ", "ae")
        texte = unicodedata.normalize("NFKD", texte)
        texte = "".join(c for c in texte if not unicodedata.combining(c))
        mots = [m for m in re.split(r"[^a-z0-9]+", texte) if m and m not in MOTS_VIDES]
        return " ".join(mots)

    def bonne_reponse(enigme, reponse):
        if enigme.get("saisie"):
            return normaliser(reponse or "") in [normaliser(a) for a in reponses_admises(enigme)]
        return reponse == enigme["answer"]

    def premiere_lettre(enigme):
        """Pouvoir de l'Encre sur une énigme à réponse libre."""
        mot = normaliser(reponses_admises(enigme)[0])
        return mot[:1].upper()

    # ------------------------------------------------------------------
    # MÉMOIRE DU MANOIR (anti-triche par sauvegarde)
    # ------------------------------------------------------------------
    def cle_porte():
        return "%s-%d" % (id_partie, manche)

    def verdict_connu():
        """Verdict déjà rendu pour cette porte (partie rechargée), ou None."""
        return persistent.verdicts.get(cle_porte())

    def memoriser_verdict(correct, misees, murmure=False):
        verdicts = dict(persistent.verdicts)
        verdicts[cle_porte()] = (correct, list(misees), murmure)
        # On ne garde que les 300 derniers verdicts
        while len(verdicts) > 300:
            del verdicts[next(iter(verdicts))]
        persistent.verdicts = verdicts
        renpy.save_persistent()

    # ------------------------------------------------------------------
    # LA BOUGIE (remplace le compteur de portes)
    # ------------------------------------------------------------------
    def portes_restantes():
        """Portes que la bougie peut encore éclairer (porte en cours comprise
        tant qu'on ne l'a pas franchie)."""
        return max(0, min(max_manches, max_manches + bonus_bougie) - manche)

    # ------------------------------------------------------------------
    # FINS
    # ------------------------------------------------------------------
    # (code, nom, comment l'obtenir : affiché tant que la fin est cachée)
    fins = [
        ("delivrance", "La délivrance", "Sortir sans commettre une seule erreur."),
        ("aube", "L'aube", "Trouver la sortie."),
        ("vrai_nom", "Le vrai nom", "Un secret dort dans le journal d'Éléonore."),
        ("mains_vides", "Les mains vides", "Perdre tous ses fragments."),
        ("gardien", "Le gardien", "Tout perdre après avoir tenu la carte complète."),
        ("minuit", "Le dernier coup de minuit", "Laisser la bougie s'éteindre."),
    ]

    def debloquer_fin(code):
        persistent.fins_vues = set(persistent.fins_vues) | {code}
        persistent.derniere_fin = code
        renpy.save_persistent()

    # ------------------------------------------------------------------
    # LE JOURNAL D'ÉLÉONORE (pages gardées d'une partie à l'autre)
    # ------------------------------------------------------------------
    pages_journal = [
        "Premier jour de ce cahier. Père dit que le monde du dehors est rempli de loups. Je n'en ai jamais vu un seul.",
        "Les portes du nord sont murées. J'ai compté les pierres : il y en a quarante. Demain, je recompterai.",
        "La gouvernante est partie cette nuit. Père dit qu'elle s'est perdue dans les couloirs. Les couloirs ne perdent personne. Ils gardent.",
        "J'ai trouvé le plan dans le bureau de Père. Il l'a lu dans mes yeux. Le lendemain, le plan était déchiré en quatre.",
        "Le manoir m'écoute. Quand je pose une question aux portes, elles répondent. Quand je me trompe, elles prennent quelque chose.",
        "Père est mort cet hiver. Les portes ne se sont pas ouvertes pour autant. Je crois que c'est moi, maintenant, qu'elles écoutent.",
        "Je ne me souviens plus de la couleur du ciel. Je parle aux voyageurs à travers le bois. Aucun ne m'a jamais demandé mon nom.",
        "Si un jour quelqu'un, devant la dernière porte, au lieu de répondre, prononce mon nom… alors peut-être que je pourrai partir, moi aussi.",
    ]

    def journal_complet():
        return len(persistent.pages_journal) >= len(pages_journal)

    def trouver_page():
        """Ajoute au journal une page encore manquante. Renvoie son numéro
        (à partir de 1), ou None si le journal est complet."""
        manquantes = [i for i in range(len(pages_journal)) if i not in persistent.pages_journal]
        if not manquantes:
            return None
        i = min(manquantes)
        persistent.pages_journal = set(persistent.pages_journal) | {i}
        renpy.save_persistent()
        return i + 1

    def dit_le_nom(reponse):
        """Le joueur tape le nom de la voix à la porte de sortie."""
        return normaliser(reponse or "") in ("eleonore", "eleonore blackwood")

    # ------------------------------------------------------------------
    # ACCESSIBILITÉ
    # ------------------------------------------------------------------
    def tx(taille):
        """Taille de texte, agrandie si l'option « Texte agrandi » est active."""
        return int(taille * 1.18) if persistent.texte_grand else taille

    def flash(transition):
        """Transition éclair, remplacée par un simple fondu en mode sans flash."""
        return Dissolve(0.4) if persistent.sans_flash else transition
