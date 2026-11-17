########################################
# LE MANOIR DES OMBRES — traduction_en.rpy
# Traduction anglaise : texte français -> texte anglais
########################################

# Pour corriger une traduction, modifier le texte de droite. Le texte de
# gauche doit rester identique, au caractère près, au texte français du jeu.

init -5 python:

    # Réponses admises au clavier en anglais (sans article ni majuscule),
    # pour les énigmes dont la réponse a plusieurs formes.
    ACCEPTE_EN.update({
        'Une pièce de monnaie': ['coin'],
        'La lettre N': ['n', 'letter n'],
        "L'obscurité": ['darkness', 'dark', 'night'],
        "L'avenir": ['future', 'tomorrow'],
        "L'homme": ['man', 'human', 'mankind', 'human being'],
        'Aucune': ['none', 'zero', '0', 'no pages'],
        'Neuf': ['nine', '9'],
        'Onze': ['eleven', '11'],
        '9 h': ['9', 'nine', '9 o clock', 'nine o clock', '9 00'],
        '9 m': ['9', '9 m', 'nine', '9 metres', '9 meters', 'nine metres', 'nine meters'],
        '10': ['10', 'ten'],
        'Votre prénom': ['name', 'first name'],
        'La lettre E': ['e', 'letter e'],
        'Une carte': ['map'],
        'Ton ombre': ['shadow'],
        "L'écho": ['echo'],
        'Le silence': ['silence'],
        'Un secret': ['secret'],
        'Éléonore': ['eleonore', 'eleanor'],
        'Sa fille': ['daughter', 'her daughter'],
        "L'âge": ['age'],
        'Un cercueil': ['coffin', 'casket'],
        'Un escalier': ['staircase', 'stairs', 'stair', 'stairway'],
        'Un fauteuil': ['armchair', 'chair'],
        'Le vin': ['wine'],
        'Une horloge': ['clock'],
        'Rien': ['nothing'],
    })

    TRAD_EN.update({
        'La pluie a effacé le chemin depuis longtemps. Vous êtes perdu, seul, dans la forêt.':
            'The rain washed the path away long ago. You are lost, alone, in the forest.',
        "Le tonnerre gronde au loin, et vos vêtements trempés collent à votre peau. Continuer ainsi n'est plus possible.":
            'Thunder rumbles in the distance, and your soaked clothes cling to your skin. You cannot go on like this.',
        "Au détour d'un sentier, un manoir se dresse, ses fenêtres hautes noyées d'obscurité, à l'exception d'une seule lueur vacillante.":
            'Around a bend in the path, a manor rises, its tall windows drowned in darkness, all but one, where a single light flickers.',
        'Sur la grille rouillée, une plaque à demi effacée : « Blackwood ». La nuit est trop noire, et la pluie trop froide, pour aller plus loin.':
            'On the rusty gate, a half-worn plaque reads: “Blackwood”. The night is too black, and the rain too cold, to go any further.',
        "La porte s'ouvre sans résistance, comme si elle vous attendait. Elle se referme derrière vous, et vous comprenez qu'elle ne se rouvrira pas.":
            'The door opens without resistance, as if it had been waiting for you. It closes behind you, and you understand it will not open again.',
        "Sous le tapis de l'entrée dépasse un parchemin déchiré. Vous le ramassez : un morceau de plan, rien qu'un.":
            'Under the entrance rug, a torn piece of parchment sticks out. You pick it up: a piece of a map, just one.',
        "Au dos, quelques lignes d'une écriture fine : [lore_depart]":
            'On the back, a few lines in a fine hand: [lore_depart]',
        "Une voix de femme s'élève des murs, incrédule : « Toi ? Tu étais sorti… Pourquoi reviens-tu ? »":
            "A woman's voice rises from the walls, in disbelief: “You? You got out… Why have you come back?”",
        "Une voix de femme s'élève des murs : « Encore toi. La dernière fois, tu es resté avec moi. Tu t'en souviens ? »":
            "A woman's voice rises from the walls: “You again. Last time, you stayed with me. Do you remember?”",
        "Une voix de femme s'élève des murs : « Je reconnais ton pas. Tu es déjà venu ici. »":
            "A woman's voice rises from the walls: “I know your footsteps. You have been here before.”",
        '[texte_visite]':
            '[texte_visite]',
        "« Les règles n'ont pas changé. Il te faut [total_pieces] morceaux pour retrouver ton chemin. »":
            '“The rules have not changed. You need [total_pieces] pieces to find your way.”',
        "Une voix de femme s'élève des murs : « Il te faut [total_pieces] morceaux pour retrouver ton chemin. À chaque porte, tu m'en offriras un. »":
            "A woman's voice rises from the walls: “You need [total_pieces] pieces to find your way. At every door, you will offer me one.”",
        '« Réponds juste, et je te le rends, avec un autre. Trompe-toi, et je le garde. »':
            '“Answer right, and I will give it back, with another. Get it wrong, and I keep it.”',
        '« Chaque morceau a son pouvoir. Celui-ci est la Lanterne : tant que tu le gardes, je te soufflerai un indice. »':
            '“Each piece has its power. This one is the Lantern: as long as you keep it, I will whisper you a hint.”',
        '« Mais le morceau que tu mises reste sous la porte… et son pouvoir avec lui. »':
            '“But the piece you wager stays under the door… and its power with it.”',
        "« Dans chaque pièce, deux portes. Celle de chêne te proposera des réponses. Celle qui murmure t'obligera à chercher seul… mais elle sait se montrer généreuse. »":
            '“In every room, two doors. The oak door will offer you answers. The whispering door will make you search alone… but it knows how to be generous.”',
        "« Ta bougie éclairera [max_manches] portes. Quand ta carte sera complète, il te restera la porte de sortie. Et si ta bougie s'éteint, ou si tes mains sont vides avant… tu resteras ici. Avec moi. »":
            '“Your candle will light [max_manches] doors. When your map is complete, the way out will remain. And if your candle dies, or your hands are empty before that… you will stay here. With me.”',
        '[texte_page]':
            '[texte_page]',
        'Le journal est complet. Une phrase, sur la dernière page, semble écrite pour vous.':
            'The diary is complete. One sentence, on the last page, seems written for you.',
        '[texte_salle]':
            '[texte_salle]',
        "« Tu as déjà répondu à cette porte », chuchote la voix. « Le manoir n'oublie rien. »":
            '“You have already answered this door,” the voice whispers. “The manor forgets nothing.”',
        '[intro_porte]':
            '[intro_porte]',
        "La voix éclate d'un rire bref : « Deux d'un coup ? Alors l'énigme sera à la hauteur de ton audace. »":
            'The voice bursts into a short laugh: “Two at once? Then the riddle will match your nerve.”',
        '[texte_mise]':
            '[texte_mise]',
        '[texte_voix]':
            '[texte_voix]',
        'La porte de sortie porte deux verrous. Chacun attend sa réponse.':
            'The way out has two locks. Each one awaits its answer.',
        "Vous retournez le sablier. Le sable remonte, et l'énigme se réécrit sous vos yeux.":
            'You turn the hourglass over. The sand flows back up, and the riddle rewrites itself before your eyes.',
        "Vous implorez la voix. La flamme de votre bougie se tord et rapetisse. « Écoute bien, car je ne le dirai qu'une fois… »":
            "You beg the voice. Your candle's flame twists and shrinks. “Listen well, for I will only say it once…”",
        "Les runes se figent. « Qui t'a dit mon nom ? » Un long silence. « Tu ne connais pas encore toute mon histoire. Réponds à l'énigme. »":
            'The runes freeze. “Who told you my name?” A long silence. “You do not know my whole story yet. Answer the riddle.”',
        'Le premier verrou cède avec un claquement sec. « Un autre », souffle la voix. « Le dernier. »':
            'The first lock gives way with a sharp click. “Another,” the voice breathes. “The last one.”',
        '[texte_victoire]':
            '[texte_victoire]',
        '[texte_gain]':
            '[texte_gain]',
        "Au dos, quelques lignes d'une écriture fine : [texte_lore]":
            'On the back, a few lines in a fine hand: [texte_lore]',
        'La flamme de votre bougie se redresse et grandit : la porte qui murmure vous offre une porte de plus.':
            "Your candle's flame straightens and grows: the whispering door grants you one more door.",
        "La porte reste close… mais le fragment de la Clé se met à briller dans votre main. L'offrande vous est rendue. La Clé, elle, s'est ternie : elle ne vous sauvera plus.":
            'The door stays shut… but the Key fragment starts to glow in your hand. Your offering is returned. The Key itself has dulled: it will not save you again.',
        '[texte_defaite]':
            '[texte_defaite]',
        '« Presque », souffle la voix. « Ta carte est de nouveau incomplète. »':
            '“Almost,” the voice breathes. “Your map is incomplete again.”',
        '[bilan]':
            '[bilan]',
        "La porte de sortie cède. Les lignes d'encre dorée de la carte s'éteignent une à une : le chemin est parcouru.":
            'The way out gives way. The golden ink lines of the map fade one by one: the path has been walked.',
        "Vous franchissez le seuil. Derrière vous, des pas légers suivent les vôtres, puis s'arrêtent sur la dernière marche.":
            'You cross the threshold. Behind you, light footsteps follow yours, then stop on the last step.',
        "« Merci », murmure la voix, si près que vous sentez un souffle sur votre nuque. « Cela faisait si longtemps que je n'avais pas vu l'aube. »":
            '“Thank you,” the voice murmurs, so close you feel a breath on your neck. “It has been so long since I saw the dawn.”',
        "Quand vous vous retournez, il n'y a personne. Seulement deux ombres sur l'herbe mouillée, et la vôtre est la seule à rester.":
            'When you turn around, there is no one. Only two shadows on the wet grass, and yours is the only one that stays.',
        'Éléonore Blackwood a enfin quitté le manoir. Fin : « La délivrance ».':
            'Eleonore Blackwood has finally left the manor. Ending: “Deliverance”.',
        "Vous sortez alors que le ciel, à l'est, commence à pâlir. Derrière vous, le manoir reprend son silence, comme s'il n'avait jamais eu de visiteur.":
            'You step out as the sky, in the east, begins to pale. Behind you, the manor returns to its silence, as if it had never had a visitor.',
        "Au loin, une voix appelle encore, très bas : « Emmène-moi… » Mais la porte s'est déjà refermée. Fin : « L'aube ».":
            'Far away, a voice still calls, very softly: “Take me with you…” But the door has already closed. Ending: “Dawn”.',
        '(Peut-être existe-t-il une autre fin, pour qui ne se tromperait jamais…)':
            '(Perhaps there is another ending, for one who never makes a mistake…)',
        '[texte_score]':
            '[texte_score]',
        "« Éléonore. » Le nom tombe dans le silence comme une pierre au fond d'un puits.":
            '“Eleonore.” The name falls into the silence like a stone into a well.',
        "Les runes de la porte s'éteignent. Puis, une à une, toutes les bougies du manoir.":
            'The runes on the door go dark. Then, one by one, every candle in the manor.',
        "« Personne… personne ne l'avait jamais dit », souffle la voix. Pour la première fois, elle ne vient pas des murs, mais de juste à côté de vous.":
            '“No one… no one had ever said it,” the voice breathes. For the first time, it does not come from the walls, but from right beside you.',
        "Quand vous franchissez la grille, le manoir derrière vous n'est plus qu'un tas de pierres mangées par le lierre, comme s'il était en ruine depuis cent ans.":
            'When you pass through the gate, the manor behind you is nothing but a heap of ivy-eaten stones, as if it had lain in ruins for a hundred years.',
        "Près de vous, quelqu'un regarde le ciel pâlir. Elle avait oublié sa couleur. Fin secrète : « Le vrai nom ».":
            'Beside you, someone watches the sky grow pale. She had forgotten its colour. Secret ending: “The True Name”.',
        'Vos mains sont vides. Il y a quelques portes encore, vous teniez pourtant la carte entière.':
            'Your hands are empty. Only a few doors ago, you held the whole map.',
        '« Tu étais si près », murmure la voix. « Moi aussi, autrefois. »':
            '“You were so close,” the voice murmurs. “So was I, once.”',
        "Une main froide se pose sur la vôtre, puis s'en va. Des pas légers s'éloignent vers l'entrée, et la grande porte s'ouvre… pour quelqu'un d'autre.":
            'A cold hand rests on yours, then leaves. Light footsteps fade toward the entrance, and the great door opens… for someone else.',
        "Désormais, c'est votre voix qui résonne dans les murs. Vous attendez le prochain voyageur.":
            'From now on, it is your voice that echoes in the walls. You wait for the next traveller.',
        'Vos mains sont vides. Il ne vous reste plus rien à offrir au manoir.':
            'Your hands are empty. You have nothing left to offer the manor.',
        "« Ne t'inquiète pas », dit la voix, presque tendre. « On s'habitue. Moi, je me suis habituée. »":
            "“Don't worry,” says the voice, almost tender. “You get used to it. I did.”",
        "Votre bougie n'est plus qu'une flaque de cire. Quelque part, une horloge sonne le dernier coup de minuit, et votre carte ne vous mènera nulle part.":
            'Your candle is nothing but a puddle of wax. Somewhere, a clock strikes the last stroke of midnight, and your map will lead you nowhere.',
        'Autour de vous, les couloirs se referment un à un, non pas dans un vacarme de pierre, mais dans un silence total, presque poli.':
            'Around you, the corridors close one by one, not with a roar of stone, but in total, almost polite silence.',
        "La dernière chose que vous voyez est la lumière de votre bougie, qui vacille, puis s'éteint. Fin : « [nom_fin] ».":
            'The last thing you see is the light of your candle, flickering, then going out. Ending: “[nom_fin]”.',
        "« C'est ta %de visite. Les murs se souviennent de toi, et moi aussi. »":
            '“This is visit number %d. The walls remember you, and so do I.”',
        "%s Une page du journal d'Éléonore (%d/%d).":
            "%s A page from Eleonore's diary (%d/%d).",
        '« %s »':
            '“%s”',
        'Vous gagnez le %s. %s':
            'You gain the %s. %s',
        "Votre bougie n'éclairera plus qu'une porte.":
            'Your candle will light only one more door.',
        'Votre bougie peut encore éclairer %d portes.':
            'Your candle can still light %d doors.',
        "La carte est complète ! Il ne reste qu'à trouver la porte de sortie. %s":
            'The map is complete! All that remains is to find the way out. %s',
        'Morceaux de carte : %d/%d. %s':
            'Map pieces: %d/%d. %s',
        'Sortie trouvée en %d portes, avec %d erreurs.':
            'Way out found in %d doors, with %d mistakes.',
        'Sortie trouvée en %d portes, avec %d erreur.':
            'Way out found in %d doors, with %d mistake.',
        'Le gardien':
            'The Keeper',
        'Les mains vides':
            'Empty Hands',
        'Le dernier coup de minuit':
            'The Last Stroke of Midnight',
        'Morceaux réunis : %d/%d.':
            'Pieces gathered: %d/%d.',
        'Entre deux lattes du plancher, une feuille arrachée dépasse.':
            'Between two floorboards, a torn sheet sticks out.',
        "Glissée dans l'entrebâillement de la porte, une feuille vous attend.":
            'Slipped into the gap of the door, a sheet awaits you.',
        'Fragment de la Lanterne':
            'Lantern Fragment',
        'Lanterne':
            'Lantern',
        'La voix vous souffle un indice.':
            'The voice whispers you a hint.',
        "« Plan du manoir Blackwood, relevé de ma main à l'automne 1847. Que nul ne s'y perde jamais. — Edmund Blackwood »":
            '“Plan of Blackwood Manor, surveyed by my own hand in the autumn of 1847. May no one ever lose their way here. — Edmund Blackwood”',
        "Fragment de l'Encre":
            'Ink Fragment',
        'Encre':
            'Ink',
        'Une mauvaise réponse est barrée (ou la première lettre révélée).':
            'One wrong answer is crossed out (or the first letter revealed).',
        "« Éléonore pose trop de questions sur le monde du dehors. J'ai fait murer les portes du nord. Elle ne partira pas comme sa mère. »":
            '“Eleonore asks too many questions about the outside world. I have had the north doors walled up. She will not leave as her mother did.”',
        'Fragment du Sablier':
            'Hourglass Fragment',
        'Sablier':
            'Hourglass',
        'Une fois par porte, vous pouvez demander une autre énigme.':
            'Once per door, you may ask for another riddle.',
        "« Père a déchiré la carte en quatre et l'a cachée dans les murs. Le soir, quand je cherche la sortie, j'entends les couloirs bouger. — É. »":
            '“Father tore the map into four and hid it in the walls. At night, when I look for the way out, I hear the corridors move. — E.”',
        'Fragment de la Clé':
            'Key Fragment',
        'Clé':
            'Key',
        'Une fois par partie, une erreur ne vous coûte rien.':
            'Once per game, a mistake costs you nothing.',
        "« Si quelqu'un lit ceci, rassemblez les morceaux et sortez. Et, je vous en supplie, emmenez-moi avec vous. — Éléonore »":
            '“If anyone reads this, gather the pieces and get out. And, I beg you, take me with you. — Eleonore”',
        'Au bout du couloir, une porte de chêne toute simple vous attend, éclairée par une bougie posée sur un guéridon. Une voix douce, presque amusée, murmure à travers le bois.':
            'At the end of the corridor, a plain oak door awaits you, lit by a candle on a small table. A soft, almost amused voice murmurs through the wood.',
        'La porte de chêne est revenue, comme si le couloir avait tourné sur lui-même. La bougie brûle toujours, et la voix semble presque indulgente.':
            'The oak door is back, as if the corridor had turned in on itself. The candle still burns, and the voice sounds almost kind.',
        'Une porte claire, presque accueillante, se dresse devant vous. Ici, le manoir paraît vouloir vous laisser une chance.':
            'A pale, almost welcoming door stands before you. Here, the manor seems willing to give you a chance.',
        "Une porte se cache au fond de la bibliothèque, ses panneaux couverts de lettres gravées. L'air sent le vieux papier, et la voix, cette fois, ne sourit plus.":
            'A door hides at the back of the library, its panels covered in carved letters. The air smells of old paper, and the voice, this time, no longer smiles.',
        "Entre deux rayonnages, la porte gravée vous attend. Les livres semblent s'être rapprochés pour mieux écouter votre réponse.":
            'Between two bookshelves, the carved door awaits you. The books seem to have leaned closer to hear your answer.',
        "La bibliothèque est plus sombre qu'avant. Sur la porte, les lettres gravées remuent à peine, comme si elles respiraient.":
            'The library is darker than before. On the door, the carved letters barely stir, as if they were breathing.',
        'Une porte noire, immense, striée de runes dorées qui pulsent comme un cœur. Derrière elle, vous le sentez, la carte attend son dernier morceau. La voix gronde, grave et patiente.':
            'A huge black door, streaked with golden runes that pulse like a heart. Behind it, you can feel it, the map awaits its last piece. The voice growls, deep and patient.',
        'La grande porte noire se dresse de nouveau. Les runes battent plus vite à votre approche : un seul morceau de plus, et la carte serait complète.':
            'The great black door rises again. The runes beat faster as you approach: one more piece, and the map would be complete.',
        "La brume rampe au pied de la porte aux runes d'or. La voix ne murmure plus : elle attend, et elle sait que vous êtes tout près.":
            'Mist creeps at the foot of the door with golden runes. The voice no longer whispers: it waits, and it knows you are very close.',
        "La carte complète vous guide jusqu'à une porte basse, couverte de signes, que vous n'aviez jamais vue. De l'autre côté, vous jureriez sentir l'air froid du dehors.":
            'The complete map leads you to a low door, covered in signs, that you had never seen. On the other side, you would swear you can feel the cold air of the outside.',
        "La porte de sortie est là, exactement où la carte l'indique. La voix tremble : « Cette fois, aucune réponse ne te sera proposée. Trouve-la seul. »":
            'The way out is there, exactly where the map says. The voice trembles: “This time, no answers will be offered. Find it alone.”',
        'Je suis blanche, je tombe du ciel en hiver et je fonds au soleil. Qui suis-je ?':
            'I am white, I fall from the sky in winter and I melt in the sun. What am I?',
        'La neige':
            'Snow',
        'La pluie':
            'Rain',
        'Le sable':
            'Sand',
        'La cendre':
            'Ash',
        'Les enfants en font des bonshommes.':
            'Children make men out of me.',
        'Je brille dans le ciel la nuit, et ma forme change au fil du mois. Qui suis-je ?':
            'I shine in the sky at night, and my shape changes over the month. What am I?',
        'La lune':
            'The moon',
        'Le soleil':
            'The sun',
        'Un nuage':
            'A cloud',
        'Un oiseau':
            'A bird',
        "On dit qu'elle est pleine, ou nouvelle.":
            'They say I am full, or new.',
        "Je porte le nom de ma propre couleur, et l'on me mange en hiver. Quel fruit suis-je ?":
            'I share my name with my own colour, and people eat me in winter. Which fruit am I?',
        "L'orange":
            'An orange',
        'La pomme':
            'An apple',
        'La poire':
            'A pear',
        'La fraise':
            'A strawberry',
        'Je suis un agrume.':
            'I am a citrus fruit.',
        'On me monte et on me descend, mais je ne bouge jamais. Qui suis-je ?':
            'You go up me and down me, yet I never move. What am I?',
        'Un escalier':
            'A staircase',
        'Un ascenseur':
            'A lift',
        'Un ballon':
            'A balloon',
        'Un cheval':
            'A horse',
        'Le hall du manoir en a un très grand.':
            "The manor's hall has a very large one.",
        'Je suis jaune, je brille dans le ciel pendant la journée et je réchauffe la terre. Qui suis-je ?':
            'I am yellow, I shine in the sky during the day and I warm the earth. What am I?',
        "Je me lève à l'est.":
            'I rise in the east.',
        "J'ai des ailes, des plumes et un bec, et je chante le matin. Qui suis-je ?":
            'I have wings, feathers and a beak, and I sing in the morning. What am I?',
        'Un chat':
            'A cat',
        'Un poisson':
            'A fish',
        'Un serpent':
            'A snake',
        'Je fais mon nid dans les arbres.':
            'I build my nest in the trees.',
        "On m'allume quand il fait noir, et je fonds doucement en brûlant. Qui suis-je ?":
            'You light me when it is dark, and I slowly melt as I burn. What am I?',
        'Une bougie':
            'A candle',
        'Une lampe':
            'A lamp',
        'Un miroir':
            'A mirror',
        'Une clé':
            'A key',
        'Je suis faite de cire.':
            'I am made of wax.',
        'Je pousse sur les branches au printemps et je tombe en automne. Qui suis-je ?':
            'I grow on branches in spring and fall in autumn. What am I?',
        'Une feuille':
            'A leaf',
        'Une pierre':
            'A stone',
        'Un nid':
            'A nest',
        'Une racine':
            'A root',
        'Je suis verte, puis rousse.':
            'I am green, then russet.',
        'Il faut me casser avant de pouvoir me manger. Qui suis-je ?':
            'You have to break me before you can eat me. What am I?',
        'Un œuf':
            'An egg',
        'Un gâteau':
            'A cake',
        'Une soupe':
            'A soup',
        'Une banane':
            'A banana',
        'La poule y est pour quelque chose.':
            'The hen has something to do with it.',
        "J'ai un pied et un chapeau, et je pousse dans la forêt après la pluie. Qui suis-je ?":
            'I have a foot and a hat, and I grow in the forest after the rain. What am I?',
        'Un champignon':
            'A mushroom',
        'Un sapin':
            'A fir tree',
        'Un écureuil':
            'A squirrel',
        'Un rocher':
            'A rock',
        "Certains sont comestibles, d'autres mortels.":
            'Some are edible, others deadly.',
        'Plus je travaille, plus je raccourcis. Je sers à écrire et à dessiner. Qui suis-je ?':
            'The more I work, the shorter I get. I am used to write and draw. What am I?',
        'Un crayon':
            'A pencil',
        'Un livre':
            'A book',
        'Une règle':
            'A ruler',
        'Une gomme':
            'An eraser',
        'On me taille.':
            'You sharpen me.',
        "Je garde la maison, j'aboie quand on frappe et je remue la queue. Qui suis-je ?":
            'I guard the house, I bark when someone knocks and I wag my tail. What am I?',
        'Un chien':
            'A dog',
        'Un hibou':
            'An owl',
        "Je suis le meilleur ami de l'homme.":
            "I am man's best friend.",
        "Dans le grenier, je tisse ma toile dans tous les coins, et j'ai huit pattes. Qui suis-je ?":
            'In the attic, I weave my web in every corner, and I have eight legs. What am I?',
        'Une araignée':
            'A spider',
        'Une fourmi':
            'An ant',
        'Un papillon':
            'A butterfly',
        'Une souris':
            'A mouse',
        'Regardez les toiles accrochées aux poutres.':
            'Look at the webs hanging from the beams.',
        "Plus on m'enlève de matière, plus je deviens grand. Qui suis-je ?":
            'The more you take away from me, the bigger I become. What am I?',
        'Un trou':
            'A hole',
        'Un mur':
            'A wall',
        'Un arbre':
            'A tree',
        'Une montagne':
            'A mountain',
        'Prenez une pelle et creusez.':
            'Take a shovel and dig.',
        "Je suis plein de trous, et pourtant je retiens l'eau. Qui suis-je ?":
            'I am full of holes, and yet I hold water. What am I?',
        'Une éponge':
            'A sponge',
        'Un seau':
            'A bucket',
        'Un filet':
            'A net',
        'Une passoire':
            'A sieve',
        'On me presse pour me vider.':
            'You squeeze me to empty me.',
        'Plus je sèche, plus je suis mouillée. Qui suis-je ?':
            'The more I dry, the wetter I get. What am I?',
        'Une serviette':
            'A towel',
        "On s'en sert en sortant du bain.":
            'You use it when you get out of the bath.',
        "Il est à vous, mais les autres s'en servent bien plus que vous. Qu'est-ce que c'est ?":
            'It belongs to you, but other people use it far more than you do. What is it?',
        'Votre prénom':
            'Your name',
        'Votre maison':
            'Your house',
        'Votre ombre':
            'Your shadow',
        'Votre voix':
            'Your voice',
        'On vous appelle par lui.':
            'People call you by it.',
        "J'ai une tête et une queue, mais pas de corps. Qui suis-je ?":
            'I have a head and a tail, but no body. What am I?',
        'Une pièce de monnaie':
            'A coin',
        'Pile ou face ?':
            'Heads or tails?',
        "Plus il y en a, moins on y voit. Qu'est-ce que c'est ?":
            'The more there is, the less you see. What is it?',
        "L'obscurité":
            'Darkness',
        'La lumière':
            'Light',
        'Le silence':
            'Silence',
        'Le bruit':
            'Noise',
        'Ce manoir en est rempli.':
            'This manor is full of it.',
        'Je suis toujours devant toi, mais tu ne me verras jamais. Qui suis-je ?':
            'I am always ahead of you, but you will never see me. What am I?',
        "L'avenir":
            'The future',
        'Le passé':
            'The past',
        'Ton reflet':
            'Your reflection',
        'Le ciel':
            'The sky',
        'Demain en fait partie.':
            'Tomorrow is part of it.',
        "J'ai des touches noires et blanches, mais je ne sais pas écrire. Qui suis-je ?":
            'I have black and white keys, but I cannot write. What am I?',
        'Un piano':
            'A piano',
        'Une machine à écrire':
            'A typewriter',
        'Un zèbre':
            'A zebra',
        'Un échiquier':
            'A chessboard',
        'On joue sur moi.':
            'People play on me.',
        'Le matin, je marche à quatre pattes ; à midi, sur deux ; le soir, sur trois. Qui suis-je ?':
            'In the morning, I walk on four legs; at noon, on two; in the evening, on three. What am I?',
        "L'homme":
            'Man',
        'Le chat':
            'The cat',
        'Le cheval':
            'The horse',
        "L'araignée":
            'The spider',
        'Le matin, le midi et le soir sont les âges de la vie.':
            'Morning, noon and evening are the ages of life.',
        'Je monte sans cesse, mais je ne redescends jamais. Qui suis-je ?':
            'I keep going up, but I never come down. What am I?',
        "L'âge":
            'Your age',
        'La marée':
            'The tide',
        'On le fête chaque année.':
            'People celebrate it every year.',
        "J'ai des dents, mais je ne mords jamais. Qui suis-je ?":
            'I have teeth, but I never bite. What am I?',
        'Un peigne':
            'A comb',
        'Un requin':
            'A shark',
        'Je passe dans les cheveux.':
            'I go through your hair.',
        "Je cours sans jambes, j'ai un lit mais je ne dors jamais. Qui suis-je ?":
            'I run without legs, I have a bed but I never sleep. What am I?',
        'Une rivière':
            'A river',
        'Le vent':
            'The wind',
        'Une horloge':
            'A clock',
        'Je finis dans la mer.':
            'I end up in the sea.',
        'Plus je vieillis au fond de cette cave, plus on me trouve bon. Qui suis-je ?':
            'The older I grow at the bottom of this cellar, the better people find me. What am I?',
        'Le vin':
            'Wine',
        'Le pain':
            'Bread',
        'Le lait':
            'Milk',
        'La soupe':
            'Soup',
        'On me garde dans un tonneau.':
            'I am kept in a barrel.',
        "On me couvre d'un drap pour me protéger, et pourtant je n'ai jamais froid. Je reçois tout le monde sans jamais me lever. Qui suis-je ?":
            'I am covered with a sheet to protect me, and yet I am never cold. I welcome everyone without ever getting up. What am I?',
        'Un fauteuil':
            'An armchair',
        'Un fantôme':
            'A ghost',
        'Un lit':
            'A bed',
        'Les meubles du grenier dorment sous des draps.':
            'The attic furniture sleeps under sheets.',
        'Dans ce couloir, le premier tableau est accroché à 1 mètre de la porte, puis il y en a un tous les 2 mètres. À quelle distance de la porte se trouve le cinquième ?':
            'In this corridor, the first painting hangs 1 metre from the door, then there is one every 2 metres. How far from the door is the fifth?',
        '9 m':
            '9 m',
        '10 m':
            '10 m',
        '11 m':
            '11 m',
        '8 m':
            '8 m',
        "Entre le premier et le cinquième, il n'y a que quatre intervalles.":
            'Between the first and the fifth, there are only four gaps.',
        "Celui qui me fabrique me vend. Celui qui m'achète ne se sert pas de moi. Celui qui se sert de moi ne me voit jamais. Qui suis-je ?":
            'The one who makes me sells me. The one who buys me does not use me. The one who uses me never sees me. What am I?',
        'Un cercueil':
            'A coffin',
        'Un cadeau':
            'A gift',
        'Une perruque':
            'A wig',
        "Celui qui s'en sert ne voit plus rien du tout.":
            'The one who uses it sees nothing at all any more.',
        "Le père d'Éléonore a cinq filles : Lala, Lélé, Lili et Lolo. Comment s'appelle la cinquième ?":
            "Eleonore's father has five daughters: Lala, Lele, Lili and Lolo. What is the fifth one called?",
        'Éléonore':
            'Eleonore',
        'Lulu':
            'Lulu',
        'Lyly':
            'Lyly',
        'Lala':
            'Lala',
        'Relisez le début de la question.':
            'Read the start of the question again.',
        'On me trouve deux fois dans « année », une fois dans « nuit », et jamais dans « jour ». Qui suis-je ?':
            'I appear twice in “banana”, once in “night”, and never in “day”. What am I?',
        'La lettre N':
            'The letter N',
        'La lettre A':
            'The letter A',
        'La lettre U':
            'The letter U',
        'La lettre I':
            'The letter I',
        'Regardez les lettres, pas le sens des mots.':
            'Look at the letters, not the meaning of the words.',
        'Un berger possède dix-sept moutons. Tous meurent, sauf neuf. Combien lui en reste-t-il ?':
            'A shepherd has seventeen sheep. All but nine die. How many does he have left?',
        'Neuf':
            'Nine',
        'Huit':
            'Eight',
        'Dix-sept':
            'Seventeen',
        'Aucun':
            'None',
        "Il n'y a aucun calcul à faire.":
            'There is no calculation to do.',
        "Devant ce portrait, la maîtresse des lieux murmure : « Je n'ai ni frère ni sœur, mais la mère de cette femme est la fille de ma mère. » Qui est sur le portrait ?":
            "Before this portrait, the lady of the house murmurs: “I have no brother or sister, but this woman's mother is my mother's daughter.” Who is in the portrait?",
        'Sa fille':
            'Her daughter',
        'Elle-même':
            'Herself',
        'Sa mère':
            'Her mother',
        'Sa nièce':
            'Her niece',
        "Fille unique, la fille de sa mère, c'est elle.":
            "An only child: her mother's daughter is herself.",
        "J'ai des aiguilles mais je ne pique pas. Je n'ai pas de jambes, et pourtant je cours sans jamais m'arrêter. Qui suis-je ?":
            'I have hands but I cannot hold. I have no legs, and yet I run without ever stopping. What am I?',
        'Un hérisson':
            'A hedgehog',
        'Une couturière':
            'A seamstress',
        'Le temps file avec moi.':
            'Time flies with me.',
        "Plus puissant que Dieu, plus méchant que le diable. Les pauvres en ont, les riches en manquent, et celui qui en mange meurt. Qu'est-ce que c'est ?":
            'More powerful than God, more evil than the devil. The poor have it, the rich need it, and if you eat it, you die. What is it?',
        'Rien':
            'Nothing',
        'Le temps':
            'Time',
        "L'argent":
            'Money',
        'La mort':
            'Death',
        'Prenez chaque phrase au pied de la lettre.':
            'Take each sentence literally.',
        "L'horloge du grand hall a deux aiguilles. Combien de fois se superposent-elles en douze heures ?":
            'The clock in the great hall has two hands. How many times do they overlap in twelve hours?',
        'Onze':
            'Eleven',
        'Douze':
            'Twelve',
        'Vingt-quatre':
            'Twenty-four',
        'Six':
            'Six',
        "Entre 11 h et 13 h, elles ne se rejoignent qu'une seule fois : à midi.":
            "Between 11 and 1 o'clock, they only meet once: at noon.",
        "Ce cadenas s'ouvre avec trois chiffres tous différents. Leur somme fait 6, leur produit aussi. Le code est le plus grand nombre possible. Quel est-il ?":
            'This padlock opens with three different digits. Their sum is 6, and so is their product. The code is the largest possible number. What is it?',
        '321':
            '321',
        '123':
            '123',
        '312':
            '312',
        '222':
            '222',
        'Trouvez les trois chiffres, puis rangez-les du plus grand au plus petit.':
            'Find the three digits, then order them from largest to smallest.',
        "Deux tomes de 100 pages sont rangés dans l'ordre sur l'étagère, dos face à vous. Un ver ronge de la première page du tome I jusqu'à la dernière page du tome II. Combien de pages traverse-t-il, couvertures non comptées ?":
            'Two 100-page volumes stand in order on the shelf, spines facing you. A worm eats from the first page of volume I to the last page of volume II. How many pages does it go through, covers not counted?',
        'Aucune':
            'None',
        '200':
            '200',
        '100':
            '100',
        '2':
            '2',
        "Sur une étagère, où se trouve la première page d'un livre dont le dos vous fait face ?":
            'On a shelf, where is the first page of a book whose spine faces you?',
        'Dans le miroir fêlé de la chambre, une horloge sans chiffres semble indiquer 3 h pile. Quelle heure est-il vraiment ?':
            "In the cracked mirror of the bedroom, a clock without numbers seems to show exactly 3 o'clock. What time is it really?",
        '9 h':
            "9 o'clock",
        '3 h':
            "3 o'clock",
        '6 h':
            "6 o'clock",
        '12 h':
            "12 o'clock",
        'Un miroir inverse la gauche et la droite.':
            'A mirror swaps left and right.',
        'Un homme monte cet escalier de 12 marches deux par deux, puis le redescend trois par trois. Combien de pas a-t-il faits en tout ?':
            'A man climbs this 12-step staircase two steps at a time, then comes back down three at a time. How many strides did he take in all?',
        '10':
            '10',
        '12':
            '12',
        '24':
            '24',
        '5':
            '5',
        'Comptez la montée, puis la descente, séparément.':
            'Count the way up, then the way down, separately.',
        "J'ai des villes sans maisons, des forêts sans arbres et des rivières sans eau. Qui suis-je ?":
            'I have cities without houses, forests without trees and rivers without water. What am I?',
        'Une carte':
            'A map',
        'Vous en tenez justement les morceaux.':
            'You are holding its pieces right now.',
        'Je te suis quand vient le jour, je te quitte quand vient la nuit. Qui suis-je ?':
            'I follow you when day comes, and I leave you when night falls. What am I?',
        'Ton ombre':
            'Your shadow',
        'Ce manoir porte mon nom.':
            'This manor bears my name.',
        "Je parle sans bouche et j'entends sans oreilles. Je n'ai pas de corps, mais je réponds à qui m'appelle. Qui suis-je ?":
            'I speak without a mouth and hear without ears. I have no body, but I answer whoever calls me. What am I?',
        "L'écho":
            'An echo',
        'Criez dans une grotte.':
            'Shout into a cave.',
        'Il suffit de prononcer mon nom pour me briser. Qui suis-je ?':
            'Just saying my name is enough to break me. What am I?',
        'Chut…':
            'Shh…',
        "Plus j'ai de gardiens, moins je suis gardé. Qui suis-je ?":
            'The more keepers I have, the less I am kept. What am I?',
        'Un secret':
            'A secret',
        'Ne le répétez à personne.':
            "Don't tell anyone.",
        "Je suis au début de l'éternité, à la fin de la vie et au milieu de la mer. Qui suis-je ?":
            'I am the beginning of eternity, the end of time and space, the beginning of every end and the end of every place. What am I?',
        'La lettre E':
            'The letter E',
        'Regardez les mots eux-mêmes, lettre par lettre.':
            'Look at the words themselves, letter by letter.',
        "Je porte des flammes sans jamais brûler, je pends au-dessus de vos têtes et je n'ai jamais touché le sol. Montrez-moi.":
            'I hold flames but never burn, I hang above your heads and I have never touched the floor. Show me.',
        'Levez les yeux.':
            'Look up.',
        'lustre':
            'chandelier',
        'escalier':
            'staircase',
        'porte de gauche':
            'left doorway',
        'porte de droite':
            'right doorway',
        'tapis':
            'carpet',
        "Je suis un long chemin rouge que tout le monde piétine, et personne ne s'en excuse. Montrez-moi.":
            'I am a long red path that everyone tramples, and no one ever apologises. Show me.',
        'Il couvre les marches et le sol.':
            'It covers the steps and the floor.',
        "Je me balance sans vent, et pourtant personne ne s'assoit sur moi. Montrez-moi.":
            'I rock without wind, and yet no one sits on me. Show me.',
        "Il attend dans l'ombre, au fond à droite.":
            'It waits in the shadows, at the back on the right.',
        'fauteuil à bascule':
            'rocking chair',
        'miroir':
            'mirror',
        'lucarne':
            'round window',
        'malles':
            'trunks',
        'canapé couvert':
            'covered sofa',
        'Je suis un œil rond dans le mur, et la lune regarde à travers moi. Montrez-moi.':
            'I am a round eye in the wall, and the moon looks through me. Show me.',
        'La lumière bleue entre par là.':
            'The blue light comes in through there.',
        "J'ai un ventre rond et je garde le vin, mais je n'ai jamais soif. Montrez-moi.":
            'I have a round belly and I keep the wine, but I am never thirsty. Show me.',
        'La bougie est posée sur lui.':
            'The candle stands on it.',
        'tonneau':
            'barrel',
        'bougie':
            'candle',
        'caisses':
            'crates',
        'flaque':
            'puddle',
        'tunnel':
            'tunnel',
        'Je pleure de la cire et je meurs en vous éclairant. Montrez-moi.':
            'I weep wax and I die while giving you light. Show me.',
        'Je suis la seule lumière de la cave.':
            'I am the only light in the cellar.',
        'Je suis une prison de verre pour une petite flamme. Montrez-moi.':
            'I am a glass prison for a small flame. Show me.',
        'Elle pend à un bras de fer forgé.':
            'It hangs from a wrought-iron arm.',
        'lanterne':
            'lantern',
        'marches du haut':
            'upper steps',
        'marches du bas':
            'lower steps',
        'colonne':
            'column',
        "Tous les pas tournent autour de moi, et je n'en fais jamais un seul. Montrez-moi.":
            'Every step turns around me, and I never take a single one. Show me.',
        "Je suis au centre de l'escalier.":
            'I am at the centre of the staircase.',
        'Je suis brisé, et pourtant je vous montre encore une autre pièce. Montrez-moi.':
            'I am broken, and yet I still show you another room. Show me.',
        'Ma surface est fêlée de partout.':
            'My surface is cracked all over.',
        'applique':
            'wall sconce',
        'voûte':
            'vaulted ceiling',
        'Je suis une petite main de métal qui tient la lumière contre le mur. Montrez-moi.':
            'I am a small metal hand that holds the light against the wall. Show me.',
        'Une seule flamme brûle dans ce couloir.':
            'A single flame burns in this corridor.',
        "Nous vous regardons passer depuis des années, mais nous n'avons jamais cligné des yeux. Montrez-nous.":
            'We have watched you walk by for years, but we have never blinked. Show us.',
        'Ils sont accrochés aux murs, dans des cadres dorés.':
            'They hang on the walls, in gilded frames.',
        'tableaux':
            'paintings',
        'porte du fond':
            'far door',
        'Je suis au bout de tout, et plus vous marchez vers moi, moins je semble approcher. Montrez-moi.':
            'I am at the end of everything, and the more you walk toward me, the less I seem to get closer. Show me.',
        'Regardez tout au bout du couloir.':
            'Look all the way down the corridor.',
        'La délivrance':
            'Deliverance',
        'Sortir sans commettre une seule erreur.':
            'Get out without making a single mistake.',
        "L'aube":
            'Dawn',
        'Trouver la sortie.':
            'Find the way out.',
        'Le vrai nom':
            'The True Name',
        "Un secret dort dans le journal d'Éléonore.":
            "A secret sleeps in Eleonore's diary.",
        'Perdre tous ses fragments.':
            'Lose all your fragments.',
        'Tout perdre après avoir tenu la carte complète.':
            'Lose everything after holding the complete map.',
        "Laisser la bougie s'éteindre.":
            'Let the candle go out.',
        "Premier jour de ce cahier. Père dit que le monde du dehors est rempli de loups. Je n'en ai jamais vu un seul.":
            'First day of this notebook. Father says the outside world is full of wolves. I have never seen a single one.',
        "Les portes du nord sont murées. J'ai compté les pierres : il y en a quarante. Demain, je recompterai.":
            'The north doors are walled up. I counted the stones: there are forty. Tomorrow, I will count again.',
        "La gouvernante est partie cette nuit. Père dit qu'elle s'est perdue dans les couloirs. Les couloirs ne perdent personne. Ils gardent.":
            'The governess left last night. Father says she got lost in the corridors. The corridors do not lose anyone. They keep.',
        "J'ai trouvé le plan dans le bureau de Père. Il l'a lu dans mes yeux. Le lendemain, le plan était déchiré en quatre.":
            "I found the plan in Father's study. He read it in my eyes. The next day, the plan was torn into four.",
        "Le manoir m'écoute. Quand je pose une question aux portes, elles répondent. Quand je me trompe, elles prennent quelque chose.":
            'The manor listens to me. When I ask the doors a question, they answer. When I am wrong, they take something.',
        "Père est mort cet hiver. Les portes ne se sont pas ouvertes pour autant. Je crois que c'est moi, maintenant, qu'elles écoutent.":
            'Father died this winter. The doors did not open for all that. I believe it is me they listen to now.',
        "Je ne me souviens plus de la couleur du ciel. Je parle aux voyageurs à travers le bois. Aucun ne m'a jamais demandé mon nom.":
            'I no longer remember the colour of the sky. I talk to travellers through the wood. None of them has ever asked my name.',
        "Si un jour quelqu'un, devant la dernière porte, au lieu de répondre, prononce mon nom… alors peut-être que je pourrai partir, moi aussi.":
            'If one day someone, before the last door, instead of answering, speaks my name… then perhaps I could leave too.',
        'Vous glissez votre morceau de carte sous la porte, en offrande.':
            'You slip your piece of the map under the door, as an offering.',
        'Le morceau quitte votre main à contrecœur ; vous le poussez sous le battant de bois.':
            'The piece leaves your hand reluctantly; you push it under the wooden door.',
        "Vous hésitez un instant, puis laissez le fragment de parchemin glisser dans l'obscurité sous la porte.":
            'You hesitate for a moment, then let the fragment of parchment slide into the darkness under the door.',
        'Vos doigts tremblent légèrement en abandonnant le fragment à la fente sombre sous la porte.':
            'Your fingers tremble slightly as you give up the fragment to the dark gap under the door.',
        "La porte s'ouvre en grand ! Votre morceau vous est rendu, et un autre glisse vers vous depuis l'obscurité.":
            'The door swings wide open! Your piece is returned to you, and another slides toward you out of the darkness.',
        'Un déclic sec résonne dans le bois. La porte cède, et un nouveau morceau de parchemin tombe à vos pieds.':
            'A sharp click echoes in the wood. The door gives way, and a new piece of parchment falls at your feet.',
        "Quelque chose, de l'autre côté, semble presque satisfait. La porte s'entrouvre, généreuse cette fois.":
            'Something, on the other side, seems almost pleased. The door opens a crack, generous this time.',
        "Les symboles gravés s'illuminent brièvement d'or avant de s'éteindre. La porte s'ouvre sans un bruit.":
            'The carved symbols briefly glow gold before going dark. The door opens without a sound.',
        'Un rire sourd résonne. Le morceau est englouti par le manoir, à jamais perdu.':
            'A muffled laugh echoes. The piece is swallowed by the manor, lost forever.',
        "La porte reste close. Sous vos pieds, le morceau de carte se dissout comme de l'encre dans l'eau.":
            'The door stays shut. At your feet, the piece of map dissolves like ink in water.',
        "Un souffle glacé s'échappe sous la porte, emportant votre offrande avec lui.":
            'An icy breath escapes from under the door, carrying your offering away with it.',
        "Le silence qui suit est pire que n'importe quel rire. Le morceau a disparu.":
            'The silence that follows is worse than any laughter. The piece is gone.',
        "Le silence du manoir n'est troublé que par le bruit de vos propres pas.":
            'The silence of the manor is broken only by the sound of your own footsteps.',
        'Quelque part, une horloge égrène des heures qui ne devraient pas exister.':
            'Somewhere, a clock counts out hours that should not exist.',
        "L'air se fait plus froid à mesure que vous avancez.":
            'The air grows colder as you move forward.',
        "Une bougie s'éteint derrière vous, sans que rien ne l'ait soufflée.":
            'A candle goes out behind you, though nothing blew on it.',
        "Vous avez l'impression, fugace, que les murs se sont légèrement déplacés.":
            'You have the fleeting feeling that the walls have moved slightly.',
        "Un courant d'air porte une odeur de parchemin brûlé.":
            'A draught carries a smell of burnt parchment.',
        'Un escalier étroit vous mène au grenier. Sous les draps, des meubles attendent un retour qui ne viendra pas.':
            'A narrow staircase leads you to the attic. Under the sheets, furniture awaits a return that will never come.',
        "Dans le grenier, un fauteuil à bascule oscille encore doucement. Personne ne s'y est assis depuis des années.":
            'In the attic, a rocking chair is still gently swaying. No one has sat in it for years.',
        "La cave sent la terre humide et le vin tourné. Quelque chose a gratté les murs, de l'intérieur.":
            'The cellar smells of damp earth and sour wine. Something has scratched the walls, from the inside.',
        'Entre les tonneaux de la cave, une bougie brûle sans jamais raccourcir.':
            'Between the barrels in the cellar, a candle burns without ever getting shorter.',
        "L'escalier en colimaçon tourne plus de fois qu'il ne devrait. Vous cessez de compter les marches.":
            'The spiral staircase turns more times than it should. You stop counting the steps.',
        "Vous descendez l'escalier de pierre, et pourtant vous arrivez à l'étage du dessus.":
            'You go down the stone staircase, and yet you arrive on the floor above.',
        "Dans le miroir du couloir, la pièce reflétée n'est pas tout à fait celle où vous vous tenez.":
            'In the corridor mirror, the reflected room is not quite the one you are standing in.',
        "Le couloir s'allonge à chaque pas. Dans le miroir, une silhouette en robe noire disparaît dès que vous la regardez.":
            'The corridor grows longer with every step. In the mirror, a figure in a black dress vanishes the moment you look at it.',
        "Vous traversez la bibliothèque. Sur un pupitre, un cahier d'enfant est resté ouvert, l'encre encore humide.":
            "You cross the library. On a lectern, a child's notebook lies open, the ink still wet.",
        "Les rayonnages de la bibliothèque montent jusqu'au plafond. Un livre tombe derrière vous, puis un autre, comme pour vous indiquer le chemin.":
            'The library shelves rise to the ceiling. A book falls behind you, then another, as if to show you the way.',
        '« Ta Lanterne ? Alors tu chercheras dans le noir. »':
            '“Your Lantern? Then you will search in the dark.”',
        '« Sans ta Lanterne, je ne te soufflerai rien. Voyons ce que tu vaux. »':
            "“Without your Lantern, I will whisper nothing. Let's see what you are worth.”",
        "« L'Encre… Tu devras lire sans aide, cette fois. »":
            '“The Ink… You will have to read without help, this time.”',
        '« Plus rien ne sera barré pour toi. Choisis bien. »':
            '“Nothing will be crossed out for you any more. Choose well.”',
        '« Tu me laisses ton Sablier. Le temps ne reviendra pas en arrière. »':
            '“You leave me your Hourglass. Time will not turn back.”',
        '« Pas de seconde chance, cette fois. Le sable est à moi. »':
            '“No second chance, this time. The sand is mine.”',
        '« La Clé ! Courageux… ou imprudent. Plus rien ne te pardonnera. »':
            '“The Key! Brave… or reckless. Nothing will forgive you now.”',
        '« Sans ta Clé, une erreur te coûtera vraiment. Tu le sais ? »':
            '“Without your Key, a mistake will really cost you. Do you know that?”',
        '« Deux fois de suite… Tu commences à me ressembler. »':
            '“Twice in a row… You are starting to resemble me.”',
        "« Tu trembles. Je l'entends à ta respiration. »":
            '“You are trembling. I can hear it in your breathing.”',
        '« Encore raté. Les murs, eux, ne se trompent jamais. »':
            '“Wrong again. The walls, at least, are never wrong.”',
        "« Tu réponds trop bien. Cela m'inquiète… et cela me plaît. »":
            '“You answer too well. It worries me… and it pleases me.”',
        "« Personne n'était allé si vite depuis longtemps. »":
            '“No one has gone this fast in a long time.”',
        '« Tu lis les portes comme moi, autrefois. »':
            '“You read the doors the way I used to.”',
        "« Tu as choisi de m'écouter. Alors cherche, dans cette pièce, ce dont je parle. »":
            '“You chose to listen to me. Then search this room for what I speak of.”',
        "La porte qui murmure s'entrouvre d'un doigt. La voix, tout contre le bois : « Ici, personne ne te proposera de réponse. »":
            "The whispering door opens a finger's width. The voice, right against the wood: “Here, no one will offer you an answer.”",
        'Historique':
            'History',
        'Sauvegarder':
            'Save',
        'Charger':
            'Load',
        'Réglages':
            'Settings',
        'Menu':
            'Menu',
        'Quel morceau risquez-vous à la porte de sortie ?':
            'Which piece will you risk at the way out?',
        'Choisissez les deux morceaux à miser':
            'Choose the two pieces to wager',
        'Quel morceau de carte allez-vous miser ?':
            'Which piece of the map will you wager?',
        'Le morceau misé reste sous la porte : son pouvoir ne vous aidera pas pour cette énigme.':
            'The piece you wager stays under the door: its power will not help you with this riddle.',
        'Pouvoir déjà utilisé.':
            'Power already used.',
        'Valider la double mise':
            'Confirm the double wager',
        'Annuler':
            'Cancel',
        'Tout risquer : miser les deux':
            'Risk it all: wager both',
        'Double mise : énigme plus difficile, mais deux morceaux gagnés si vous répondez juste. Une erreur vous coûte les deux.':
            'Double wager: a harder riddle, but two pieces won if you answer right. A mistake costs you both.',
        'Lanterne : ':
            'Lantern: ',
        'La voix : ':
            'The voice: ',
        'Encre : la réponse commence par « %s ».':
            'Ink: the answer starts with “%s”.',
        'Tapez votre réponse puis appuyez sur Entrée.':
            'Type your answer, then press Enter.',
        'Répondre':
            'Answer',
        'Retourner le sablier (autre énigme)':
            'Turn the hourglass (another riddle)',
        'Implorer un indice (la bougie raccourcit)':
            'Beg for a hint (the candle shortens)',
        'Deux portes se font face. Laquelle ouvrez-vous ?':
            'Two doors face each other. Which one do you open?',
        'Votre bougie peut encore éclairer %d portes après celle-ci.':
            'Your candle can still light %d doors after this one.',
        'Votre bougie peut encore éclairer une porte après celle-ci.':
            'Your candle can still light one door after this one.',
        'Votre bougie vit sa dernière porte.':
            'Your candle is living its last door.',
        'Indice : ':
            'Hint:',
        "Cliquez sur l'objet, dans la pièce.":
            'Click on the object, in the room.',
        'Porte %d':
            'Door %d',
        'Bougie : %d':
            'Candle: %d',
        'Carte %d/%d':
            'Map %d/%d',
        'Pouvoirs : ':
            'Powers:',
        'Le plan du manoir Blackwood':
            'The plan of Blackwood Manor',
        'Notes au dos des fragments':
            'Notes on the back of the fragments',
        "D'autres notes attendent sur les morceaux perdus…":
            'More notes await on the lost pieces…',
        'Fermer':
            'Close',
        'Commencer':
            'Start',
        'Secrets du manoir':
            'Secrets of the Manor',
        'Quitter':
            'Quit',
        'Fins découvertes : %d/%d':
            'Endings found: %d/%d',
        "Journal d'Éléonore : %d/%d pages":
            "Eleonore's diary: %d/%d pages",
        'Fins':
            'Endings',
        "Journal d'Éléonore":
            "Eleonore's Diary",
        'Galerie':
            'Gallery',
        '« ??? »':
            '“???”',
        'Piste : ':
            'Clue:',
        'Page %d.':
            'Page %d.',
        "Cette page n'a pas encore été retrouvée.":
            'This page has not been found yet.',
        'Cliquez pour fermer':
            'Click to close',
        'Retour':
            'Back',
        'Menu principal':
            'Main menu',
        'Sauvegarder votre partie':
            'Save your game',
        'Charger une partie':
            'Load a game',
        '%d/%m/%Y - %H:%M':
            '%m/%d/%Y - %H:%M',
        'Emplacement vide':
            'Empty slot',
        "Rien à relire pour l'instant.":
            'Nothing to read back yet.',
        'Vitesse du texte':
            'Text speed',
        'Couper tous les sons':
            'Mute all sounds',
        'Langue':
            'Language',
        'Accessibilité':
            'Accessibility',
        'Texte agrandi':
            'Larger text',
        'Sans flash ni secousse':
            'No flashes or shaking',
        'Oui':
            'Yes',
        'Non':
            'No',
        'La porte de chêne':
            'The oak door',
        'Une énigme, et quelques réponses gravées dans le bois. Il suffit de choisir la bonne.':
            'A riddle, and a few answers carved into the wood. You only have to choose the right one.',
        'La porte qui murmure':
            'The whispering door',
        'Aucune réponse proposée : fouillez la pièce, ou trouvez le mot seul. Si vous répondez juste, la bougie gagne une porte et une page du journal vous attend.':
            'No answers offered: search the room, or find the word on your own. If you answer right, the candle gains a door and a diary page awaits you.',
        'La forêt':
            'The forest',
        'Le manoir':
            'The manor',
        'Le hall':
            'The hall',
        'La galerie des portraits':
            'The portrait gallery',
        'Le couloir au miroir':
            'The mirror corridor',
        "L'escalier":
            'The staircase',
        'Le grenier':
            'The attic',
        'La cave':
            'The cellar',
        'La porte gravée':
            'The carved door',
        'La porte aux runes':
            'The rune door',
        'La porte de sortie':
            'The way out',
        'La bibliothèque':
            'The library',
        "La chambre d'Éléonore":
            "Eleonore's room",
        'La nuit sans fin':
            'The endless night',
        'Ambiance':
            'Ambience',
        'Effets sonores':
            'Sound effects',
    })
