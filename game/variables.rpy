########################################
# LE MANOIR-LABYRINTHE — variables.rpy
# Variables globales et données des énigmes
########################################

default score = 0
default total_pieces = 10         # nombre total de morceaux pour compléter la carte
default pieces_owned = []         # liste des pièces possédées, ex: ["piece_01", "piece_03"]
default door_index = 0            # porte actuelle dans doors_data

init python:

    # Chaque porte = une énigme à choix multiples.
    # "choices"  : liste de 4 propositions (texte affiché sur les boutons)
    # "correct"  : index (0 à 3) de la bonne réponse dans "choices"
    # "reward_piece" : pièce de carte obtenue en cas de bonne réponse
    doors_data = [
        {
            "id": "door_01",
            "bg": "bg_corridor_01",
            "intro": "Une porte de chêne sculptée grince devant vous, ses gonds rouillés protestant dans le silence. Des visages peints vous observent depuis les cadres alignés le long du couloir, et une voix, à peine audible, murmure une énigme entre les lattes du bois.",
            "riddle": "Je n'ai pas de corps mais je grandis, pas de poumons mais j'ai besoin d'air. Qui suis-je ?",
            "choices": ["Le vent", "Le feu", "Le temps", "L'ombre"],
            "correct": 1,
            "reward_piece": "piece_02",
        },
        {
            "id": "door_02",
            "bg": "bg_library",
            "intro": "Dans la bibliothèque poussiéreuse, un livre s'ouvre seul sur une page couverte d'une écriture ancienne. L'air sent le vieux papier et la cire fondue ; quelque chose, ici, attend une réponse.",
            "riddle": "Plus je suis grand, moins je pèse. Qui suis-je ?",
            "choices": ["Un trou", "Un nuage", "Un rêve", "Un écho"],
            "correct": 0,
            "reward_piece": "piece_03",
        },
        {
            "id": "door_03",
            "bg": "bg_stairs",
            "intro": "L'escalier en colimaçon semble ne jamais finir, chaque marche craquant sous vos pas comme pour vous avertir. Une porte basse, à mi-hauteur, porte une énigme gravée à même la pierre.",
            "riddle": "On me lance, je vole, mais je ne reviens jamais tout seul. Qui suis-je ?",
            "choices": ["Une flèche", "Un caillou", "Un oiseau", "Une plume"],
            "correct": 1,
            "reward_piece": "piece_04",
        },
        {
            "id": "door_04",
            "bg": "bg_cellar",
            "intro": "La cave sent l'humidité et la cire fondue. Des tonneaux effondrés bordent un mur suintant, et sur la porte close au fond, des mots à peine lisibles vous mettent au défi.",
            "riddle": "Plus j'ai de gardiens, moins je suis gardé. Qui suis-je ?",
            "choices": ["Un secret", "Un trésor", "Un château", "Un mensonge"],
            "correct": 0,
            "reward_piece": "piece_05",
        },
        {
            "id": "door_05",
            "bg": "bg_corridor_02",
            "intro": "Un miroir fendu reflète une pièce qui n'existe pas, son tain écaillé renvoyant une image légèrement décalée de la vôtre. La porte, juste à côté, semble attendre que vous répondiez à son reflet.",
            "riddle": "Je nais le soir et je meurs le matin. Qui suis-je ?",
            "choices": ["La lune", "La nuit", "La bougie", "Le rêve"],
            "correct": 1,
            "reward_piece": "piece_06",
        },
        {
            "id": "door_06",
            "bg": "bg_door_generic",
            "intro": "Une porte sans poignée, gravée de symboles que vous ne reconnaissez pas, se dresse au bout d'un renfoncement sombre. Une seule ligne de lumière filtre sous le battant.",
            "riddle": "On me trouve une fois dans une minute, deux fois dans un moment, mais jamais dans mille ans. Quelle lettre suis-je ?",
            "choices": ["La lettre M", "La lettre N", "La lettre T", "La lettre S"],
            "correct": 0,
            "reward_piece": "piece_07",
        },
        {
            "id": "door_07",
            "bg": "bg_attic",
            "intro": "Le grenier est glacial, l'air chargé de poussière et de vieux tissus. Chaque planche grince sous vos pas, comme pour prévenir la maison de votre présence.",
            "riddle": "Je n'ai ni yeux, ni oreilles, ni bouche, mais je vous suis partout où la lumière va. Qui suis-je ?",
            "choices": ["Un fantôme", "Une ombre", "Un reflet", "Un souvenir"],
            "correct": 1,
            "reward_piece": "piece_08",
        },
        {
            "id": "door_08",
            "bg": "bg_corridor_01",
            "intro": "Une porte plus petite que les autres, presque cachée sous une tenture élimée, semble hésiter à s'ouvrir. Le silence, ici, est plus épais qu'ailleurs.",
            "riddle": "Je suis toujours devant toi, mais tu ne me verras jamais. Qui suis-je ?",
            "choices": ["Le passé", "L'avenir", "Le présent", "Le destin"],
            "correct": 1,
            "reward_piece": "piece_09",
        },
        {
            "id": "door_09",
            "bg": "bg_secret_room",
            "intro": "La dernière porte avant la sortie. L'air lui-même semble retenir son souffle, et une odeur d'encre fraîche flotte, incongrue, dans cette pièce oubliée.",
            "riddle": "Plus je sèche, plus je deviens mouillé. Qui suis-je ?",
            "choices": ["Une serviette", "Une éponge", "Un miroir", "Un livre"],
            "correct": 0,
            "reward_piece": "piece_10",
        },
    ]
