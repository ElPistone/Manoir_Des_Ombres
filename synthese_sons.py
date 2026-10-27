"""Fabrique tous les sons du jeu par synthèse (aucun fichier externe, aucun droit d'auteur).

Usage : python synthese_sons.py        -> écrit les .ogg dans game/audio/
Nécessite numpy, et ffmpeg dans le PATH pour l'encodage en Ogg Vorbis.
"""
import os
import subprocess
import tempfile
import wave

import numpy as np

SR = 44100
RACINE = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(RACINE, "game", "audio")
rng = np.random.default_rng(1745)


## Outils ------------------------------------------------------------

def t(duree):
    return np.arange(int(duree * SR)) / SR


def bruit(duree):
    return rng.standard_normal(int(duree * SR))


def filtre(x, bas=None, haut=None):
    """Filtre passe-bande par FFT (bas/haut en Hz, None = pas de limite)."""
    spectre = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    gain = np.ones_like(f)
    if bas:
        gain *= 1 / (1 + (bas / np.maximum(f, 1e-3)) ** 4)
    if haut:
        gain *= 1 / (1 + (f / haut) ** 4)
    return np.fft.irfft(spectre * gain, len(x))


def norm(x, crete=0.9):
    m = np.max(np.abs(x))
    return x * (crete / m) if m > 0 else x


def boucle(x, fondu=2.0):
    """Rend un son bouclable : la fin se fond dans le début."""
    n = int(fondu * SR)
    debut, fin = x[:n], x[-n:]
    rampe = np.linspace(0, 1, n)
    x = x[n:].copy()
    x[-n:] = fin * (1 - rampe) + debut * rampe
    return x


def stereo(g, d=None):
    return np.stack([g, g if d is None else d], axis=1)


def place(base, son, debut):
    i = int(debut * SR)
    fin = min(len(base), i + len(son))
    base[i:fin] += son[: fin - i]
    return base


def cloche(freq, duree, decroissance=2.5):
    """Cloche : partiels inharmoniques à décroissance exponentielle."""
    tt = t(duree)
    s = np.zeros_like(tt)
    for rapport, amp in [(1, 1.0), (2.76, 0.45), (5.4, 0.25), (8.93, 0.12)]:
        s += amp * np.sin(2 * np.pi * freq * rapport * tt) * np.exp(-tt * decroissance * rapport ** 0.5)
    return s * np.minimum(tt / 0.004, 1)


def tonnerre(duree=6.0):
    brun = np.cumsum(bruit(duree))
    brun = filtre(brun - np.mean(brun), bas=25, haut=220)
    tt = t(duree)
    env = np.minimum(tt / 0.08, 1) * np.exp(-tt / 1.6)
    craquement = filtre(bruit(duree), bas=300, haut=2500) * np.exp(-tt / 0.25)
    grondement = 1 + 0.6 * np.sin(2 * np.pi * 1.3 * tt) * np.exp(-tt / 2)
    return norm(brun * env * grondement) + 0.25 * norm(craquement)


def ecrire(nom, data):
    os.makedirs(SORTIE, exist_ok=True)
    data = np.clip(data, -1, 1)
    if data.ndim == 1:
        data = stereo(data)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        chemin_wav = tmp.name
    with wave.open(chemin_wav, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((data * 32767).astype("<i2").tobytes())
    cible = os.path.join(SORTIE, nom + ".ogg")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", chemin_wav,
                    "-c:a", "libvorbis", "-q:a", "4", cible], check=True)
    os.remove(chemin_wav)
    print("%-22s %5.1f s  %4d Ko" % (nom, len(data) / SR, os.path.getsize(cible) // 1024))


## Ambiances (bouclées) ---------------------------------------------

def ambiance_orage():
    d = 42.0
    pluie_g = filtre(bruit(d), bas=900, haut=9000)
    pluie_d = filtre(bruit(d), bas=900, haut=9000)
    houle = 0.8 + 0.2 * np.sin(2 * np.pi * t(d) / 7.0)
    gouttes = np.zeros(int(d * SR))
    for _ in range(900):
        place(gouttes, filtre(bruit(0.02), bas=2000, haut=7000) * np.exp(-t(0.02) / 0.004) * rng.uniform(0.2, 1),
              rng.uniform(0, d - 0.05))
    base = norm(pluie_g * houle) * 0.35, norm(pluie_d * houle) * 0.35
    g, dr = base[0] + 0.15 * gouttes, base[1] + 0.15 * np.roll(gouttes, 3000)
    for debut, force in [(6.0, 0.55), (21.0, 0.8), (33.0, 0.45)]:
        tn = tonnerre(7.0) * force
        place(g, tn, debut)
        place(dr, tn * 0.85, debut + 0.01)
    return stereo(boucle(norm(g, 0.7)), boucle(norm(dr, 0.7)))


def nappe(d, notes, vent=0.25, battement=0.0):
    tt = t(d)
    s = np.zeros_like(tt)
    for i, f in enumerate(notes):
        lfo = 0.6 + 0.4 * np.sin(2 * np.pi * tt / (9 + 4 * i) + i)
        s += lfo * (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.003 * tt + 1))
    souffle = filtre(bruit(d), bas=150, haut=900) * (0.5 + 0.5 * np.sin(2 * np.pi * tt / 11))
    s = norm(s) * 0.55 + norm(souffle) * vent
    if battement:
        coeur = np.zeros_like(tt)
        periode = 60.0 / battement
        temps = 0.0
        while temps < d - 1:
            for decal, amp in [(0.0, 1.0), (0.28, 0.7)]:
                tb = t(0.25)
                coup = amp * np.sin(2 * np.pi * (55 - 25 * tb) * tb) * np.exp(-tb / 0.06)
                place(coeur, coup, temps + decal)
            temps += periode
        s = s + 0.6 * norm(coeur)
    return boucle(norm(s, 0.6))


def ambiance_manoir():
    return nappe(48.0, [55.0, 82.4, 110.0, 164.8])


def ambiance_tension():
    return nappe(40.0, [49.0, 51.9, 98.0, 146.8], vent=0.3, battement=72)


## Bruitages ---------------------------------------------------------

def porte_grince():
    d = 2.4
    tt = t(d)
    s = np.zeros_like(tt)
    temps, i = 0.05, 0
    while temps < 1.8:
        frequence = 35 + 55 * np.sin(np.pi * temps / 1.8) + rng.uniform(-6, 6)
        clic = filtre(bruit(0.012), bas=400, haut=2600) * np.exp(-t(0.012) / 0.003)
        place(s, clic * (0.6 + 0.4 * np.sin(temps * 9)), temps)
        temps += 1 / frequence
        i += 1
    resonance = np.zeros_like(tt)
    for f in (610, 940, 1480):
        resonance += np.sin(2 * np.pi * f * tt)
    s = filtre(s, bas=300, haut=3000) * (1 + 0.3 * resonance / 3)
    choc = np.sin(2 * np.pi * (70 - 30 * t(0.5)) * t(0.5)) * np.exp(-t(0.5) / 0.09)
    place(s, norm(choc) * 0.6 * np.max(np.abs(s)), 1.85)
    return norm(s, 0.8)


def parchemin():
    d = 0.9
    s = np.zeros(int(d * SR))
    for _ in range(14):
        duree = rng.uniform(0.03, 0.12)
        frotte = filtre(bruit(duree), bas=1800, haut=8000) * np.hanning(int(duree * SR))
        place(s, frotte * rng.uniform(0.3, 1), rng.uniform(0, d - duree))
    return norm(s * np.exp(-t(d) / 0.6), 0.6)


def bonne_reponse():
    s = np.zeros(int(3.2 * SR))
    for i, f in enumerate([659.3, 784.0, 1046.5, 1318.5]):
        place(s, cloche(f, 2.8, 1.6), 0.09 * i)
    return norm(s, 0.75)


def mauvaise_reponse():
    d = 3.0
    tt = t(d)
    boom = np.sin(2 * np.pi * (60 * np.exp(-tt / 0.8) + 30) * tt) * np.exp(-tt / 0.7)
    grappe = sum(np.sin(2 * np.pi * f * tt) for f in (146.8, 155.6, 220.0)) * np.exp(-tt / 1.1)
    souffle = filtre(bruit(d), bas=80, haut=600) * np.exp(-tt / 0.5)
    return norm(norm(boom) + 0.35 * norm(grappe) + 0.3 * norm(souffle), 0.85)


def victoire():
    d = 6.0
    s = np.zeros(int(d * SR))
    for i, f in enumerate([523.3, 659.3, 784.0, 1046.5, 1318.5, 1568.0]):
        place(s, cloche(f, 4.0, 1.0), 0.16 * i)
    tt = t(d)
    pad = sum(np.sin(2 * np.pi * f * tt) for f in (261.6, 329.6, 392.0)) * np.minimum(tt / 1.0, 1) * np.exp(-tt / 3.0)
    return norm(norm(s) + 0.35 * norm(pad), 0.8)


def defaite():
    d = 6.0
    tt = t(d)
    glisse = np.sin(2 * np.pi * np.cumsum(110 * np.exp(-tt / 3.0) + 30) / SR)
    glisse *= np.minimum(tt / 0.3, 1) * np.exp(-tt / 2.2)
    vent = filtre(bruit(d), bas=100, haut=700) * np.minimum(tt / 1.5, 1) * np.exp(-tt / 2.5)
    return norm(norm(glisse) + 0.45 * norm(vent), 0.8)


def bougie_souffle():
    d = 1.0
    tt = t(d)
    s = filtre(bruit(d), bas=300, haut=2500) * np.sin(np.pi * np.minimum(tt / 0.6, 1)) ** 2
    return norm(s, 0.6)


def clic():
    d = 0.08
    tt = t(d)
    s = np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt / 0.008) + 0.4 * filtre(bruit(d), bas=2000) * np.exp(-tt / 0.004)
    return norm(s, 0.35)


if __name__ == "__main__":
    for nom, fabrique in [
        ("ambiance_orage", ambiance_orage),
        ("ambiance_manoir", ambiance_manoir),
        ("ambiance_tension", ambiance_tension),
        ("tonnerre", lambda: norm(tonnerre(6.0), 0.9)),
        ("porte_grince", porte_grince),
        ("parchemin", parchemin),
        ("bonne_reponse", bonne_reponse),
        ("mauvaise_reponse", mauvaise_reponse),
        ("victoire", victoire),
        ("defaite", defaite),
        ("bougie_souffle", bougie_souffle),
        ("clic", clic),
    ]:
        ecrire(nom, fabrique())
