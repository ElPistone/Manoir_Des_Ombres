"""Fabrique game/images/ui/frame_dialogue_bas.jpg (1240x230) à partir de frame_dialogue.jpg.

On garde la bande du haut, une bande centrale et la bande du bas de l'image mise à
l'échelle, raccordées par un fondu : les ornements ne sont jamais déformés.
Usage : python fabriquer_cadre_dialogue.py [largeur] [hauteur]
"""
import sys
from PIL import Image
import os
RACINE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(RACINE, "game", "images", "ui", "frame_dialogue.jpg")
CIBLE = os.path.join(RACINE, "game", "images", "ui", "frame_dialogue_bas.jpg")
W = int(sys.argv[1]) if len(sys.argv) > 1 else 1240
H = int(sys.argv[2]) if len(sys.argv) > 2 else 230
src = Image.open(SOURCE).convert('RGB')
# Retire la marge noire autour du filet doré
src = src.crop((18, 18, src.width - 22, src.height - 24))
src = src.resize((W, round(src.height * W / src.width)), Image.LANCZOS)
sh = src.height
band, ov = (H - 40) // 2 + 10, 20          # hauteur des bandes haut/bas, recouvrement
mid_h = H - 2 * band + 2 * ov
top = src.crop((0, 0, W, band))
bot = src.crop((0, sh - band, W, sh))
mid = src.crop((0, sh // 2 - mid_h // 2, W, sh // 2 - mid_h // 2 + mid_h))
out = Image.new('RGB', (W, H))
out.paste(mid, (0, band - ov))
def fondu(img, haut):
    m = Image.new('L', img.size, 255)
    for y in range(ov):
        v = int(255 * y / ov)
        for_y = (img.height - 1 - y) if haut else y
        m.paste(v, (0, for_y, img.width, for_y + 1))
    return m
out.paste(top, (0, 0), fondu(top, True))
out.paste(bot, (0, H - band), fondu(bot, False))
out.save(CIBLE, quality=92)
print(CIBLE, out.size)
