"""Nettoie les images générées par IA qui simulent la transparence.

Les générateurs d'images dessinent souvent un faux damier gris/blanc (ou un
fond blanc uni) à la place d'un vrai canal alpha. Ce script :
  - remplit le fond depuis les bords (damier ou blanc) et le rend transparent ;
  - recadre l'élément utile ;
  - réduit l'image à une taille raisonnable et l'enregistre en .webp.

Usage :
    python outils/nettoyer_assets.py SOURCE.png SORTIE.webp [taille_max]
    python outils/nettoyer_assets.py --sombre SOURCE.png SORTIE.webp [taille_max]
        (--sombre : damier noir et gris foncé, retiré partout où il apparaît)
    python outils/nettoyer_assets.py --fond SOURCE.jpg SORTIE.jpg
        (--fond : pour un décor plein écran entouré de damier, recadre
         l'image utile et la remet en 1920x1080)

Nécessite Pillow : pip install pillow
"""
import sys
from collections import deque

from PIL import Image, ImageChops, ImageFilter


def masque_fond(img, seuil_lum=150, seuil_sat=22):
    """Masque (True = fond) des pixels clairs et gris reliés au bord."""
    rgb = img.convert("RGB")
    w, h = rgb.size
    px = rgb.load()

    def est_fond(x, y):
        r, g, b = px[x, y]
        return min(r, g, b) >= seuil_lum and max(r, g, b) - min(r, g, b) <= seuil_sat

    fond = [[False] * w for _ in range(h)]
    file = deque()
    for x in range(w):
        file.append((x, 0))
        file.append((x, h - 1))
    for y in range(h):
        file.append((0, y))
        file.append((w - 1, y))
    while file:
        x, y = file.popleft()
        if fond[y][x] or not est_fond(x, y):
            continue
        fond[y][x] = True
        if x > 0:
            file.append((x - 1, y))
        if x < w - 1:
            file.append((x + 1, y))
        if y > 0:
            file.append((x, y - 1))
        if y < h - 1:
            file.append((x, y + 1))
    return fond


def alpha_gris(img, seuil_sat=6):
    """Alpha à 0 pour tous les pixels presque parfaitement gris (damier sombre),
    où qu'ils soient : utile quand le damier passe aussi à l'intérieur de l'objet."""
    r, g, b = img.convert("RGB").split()
    maxi = ImageChops.lighter(ImageChops.lighter(r, g), b)
    mini = ImageChops.darker(ImageChops.darker(r, g), b)
    sat = ImageChops.subtract(maxi, mini)
    alpha = sat.point(lambda v: 0 if v <= seuil_sat else 255)
    return alpha.filter(ImageFilter.MedianFilter(5))


def detourer(source, sortie, taille_max=512, sombre=False):
    img = Image.open(source).convert("RGBA")
    w, h = img.size
    if sombre:
        alpha = alpha_gris(img)
    else:
        fond = masque_fond(img)
        alpha = Image.new("L", (w, h), 255)
        ap = alpha.load()
        for y in range(h):
            ligne = fond[y]
            for x in range(w):
                if ligne[x]:
                    ap[x, y] = 0
    # Bord adouci : on ronge d'un pixel puis on floute légèrement
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1))
    img.putalpha(alpha)
    img = img.crop(alpha.getbbox())
    img.thumbnail((taille_max, taille_max), Image.LANCZOS)
    img.save(sortie, quality=88, method=6)
    print("%s -> %s %s" % (source, sortie, img.size))


def recadrer_fond(source, sortie, largeur=1920, hauteur=1080, marge=6):
    img = Image.open(source).convert("RGB")
    fond = masque_fond(img)
    w, h = img.size
    xs = [x for x in range(w) if not all(fond[y][x] for y in range(0, h, 4))]
    ys = [y for y in range(h) if not all(fond[y][x] for x in range(0, w, 4))]
    boite = (xs[0] + marge, ys[0] + marge, xs[-1] - marge, ys[-1] - marge)
    img = img.crop(boite)
    # Remplit 1920x1080 sans déformer (mode « cover »)
    echelle = max(largeur / img.width, hauteur / img.height)
    img = img.resize((round(img.width * echelle), round(img.height * echelle)), Image.LANCZOS)
    x0, y0 = (img.width - largeur) // 2, (img.height - hauteur) // 2
    img = img.crop((x0, y0, x0 + largeur, y0 + hauteur))
    img.save(sortie, quality=88, optimize=True)
    print("%s -> %s (zone utile %s)" % (source, sortie, boite))


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "--fond":
        recadrer_fond(sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 4 and sys.argv[1] == "--sombre":
        detourer(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 512, sombre=True)
    elif len(sys.argv) >= 3:
        detourer(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 512)
    else:
        print(__doc__)
