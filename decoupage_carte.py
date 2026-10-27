"""Découpe game/images/map/map_full.png en fragments et génère positions_carte.rpy.

Usage : python decoupage_carte.py [colonnes] [lignes]   (par défaut 2 x 2 = 4 fragments)
Nécessite Pillow : pip install pillow
"""
import os
import sys

from PIL import Image

RACINE = os.path.dirname(os.path.abspath(__file__))
CARTE = os.path.join(RACINE, "game", "images", "map", "map_full.png")
DOSSIER_SORTIE = os.path.join(RACINE, "game", "images", "map")
FICHIER_POSITIONS = os.path.join(RACINE, "game", "positions_carte.rpy")


def main():
    colonnes = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    lignes = int(sys.argv[2]) if len(sys.argv) > 2 else 2

    carte = Image.open(CARTE)
    largeur, hauteur = carte.size
    positions = {}

    for n in range(colonnes * lignes):
        col, lig = n % colonnes, n // colonnes
        x0, y0 = col * largeur // colonnes, lig * hauteur // lignes
        x1, y1 = (col + 1) * largeur // colonnes, (lig + 1) * hauteur // lignes
        pid = "piece_%02d" % (n + 1)
        carte.crop((x0, y0, x1, y1)).save(os.path.join(DOSSIER_SORTIE, pid + ".png"), optimize=True)
        positions[pid] = {"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0}

    with open(FICHIER_POSITIONS, "w", encoding="utf-8") as f:
        f.write("# Fichier généré par decoupage_carte.py, ne pas modifier à la main.\n")
        f.write("init python:\n")
        f.write("    map_full_width = %d\n" % largeur)
        f.write("    map_full_height = %d\n" % hauteur)
        f.write("    map_pieces_positions = {\n")
        for pid, p in positions.items():
            f.write("        %r: %r,\n" % (pid, p))
        f.write("    }\n")

    print("%d fragments écrits dans %s" % (len(positions), DOSSIER_SORTIE))


if __name__ == "__main__":
    main()
