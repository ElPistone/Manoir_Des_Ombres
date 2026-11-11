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
# - une fois la carte complète (4 fragments), il reste la PORTE DE SORTIE :
#   une énigme à réponse libre ; une erreur coûte encore un fragment ;
# - défaite s'il n'a plus de fragment à miser, ou après 12 portes.
# La difficulté suit le nombre de fragments possédés :
# 1 -> niveau 0, 2 -> niveau 1, 3 -> niveau 2, 4 -> niveau 3 (sortie).
define total_pieces = 4           # fragments nécessaires pour reconstituer la carte
define max_manches = 12           # nombre maximum de portes
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

# Mémoire du manoir : le verdict de chaque porte déjà répondue. Recharger une
# sauvegarde faite devant une énigme ne permet donc pas de changer de réponse.
default persistent.verdicts = {}
# Fins découvertes (affichées sur l'écran titre)
default persistent.fins_vues = set()

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

    def tirer_enigme(niv, deja_vues, sauf=None):
        """Tire une énigme du niveau donné, pas encore posée si possible
        (et différente de « sauf »), et renvoie (énigme, réponses mélangées)."""
        toutes = enigmes_par_niveau[niv]
        pool = [e for e in toutes if e["riddle"] not in deja_vues and e is not sauf]
        if not pool:
            pool = [e for e in toutes if e is not sauf] or toutes
        enigme = renpy.random.choice(pool)
        choix = list(enigme.get("choices", []))
        renpy.random.shuffle(choix)
        return enigme, choix

    def reponse_barree(enigme, choix):
        """Pouvoir de l'Encre : une mauvaise réponse à barrer."""
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
            return normaliser(reponse or "") in [normaliser(a) for a in enigme["accepte"]]
        return reponse == enigme["answer"]

    def premiere_lettre(enigme):
        """Pouvoir de l'Encre sur une énigme à réponse libre."""
        mot = normaliser(enigme["accepte"][0])
        return mot[:1].upper()

    # ------------------------------------------------------------------
    # MÉMOIRE DU MANOIR (anti-triche par sauvegarde)
    # ------------------------------------------------------------------
    def cle_porte():
        return "%s-%d" % (id_partie, manche)

    def verdict_connu():
        """Verdict déjà rendu pour cette porte (partie rechargée), ou None."""
        return persistent.verdicts.get(cle_porte())

    def memoriser_verdict(correct, misees):
        verdicts = dict(persistent.verdicts)
        verdicts[cle_porte()] = (correct, list(misees))
        # On ne garde que les 300 derniers verdicts
        while len(verdicts) > 300:
            del verdicts[next(iter(verdicts))]
        persistent.verdicts = verdicts
        renpy.save_persistent()

    # ------------------------------------------------------------------
    # FINS
    # ------------------------------------------------------------------
    fins = [
        ("delivrance", "La délivrance"),
        ("aube", "L'aube"),
        ("mains_vides", "Les mains vides"),
        ("minuit", "Le dernier coup de minuit"),
    ]

    def debloquer_fin(code):
        persistent.fins_vues = set(persistent.fins_vues) | {code}
        renpy.save_persistent()
