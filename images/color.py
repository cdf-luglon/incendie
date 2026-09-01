import colorsys
from PIL import Image

def vert_vers_rouge(chemin_entree, chemin_sortie):
    img = Image.open(chemin_entree).convert("RGBA")
    donnees = img.getdata()

    nouveaux_pixels = []
    for r, g, b, a in donnees:
        # Si le pixel est transparent, on le laisse tel quel
        if a == 0:
            nouveaux_pixels.append((r, g, b, a))
            continue

        # Conversion en espace HSV (Teinte, Saturation, Valeur)
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

        # Si le pixel est vert (teinte entre 60° et 170°) et saturé (pas du blanc/gris)
        # Teinte verte normalisée : ~0.20 à 0.48
        if 0.18 <= h <= 0.48 and s > 0.15:
            # On remplace la teinte par le rouge feu (environ 6° -> 0.018)
            nouvelle_teinte = 0.018
            
            # On booste légèrement la saturation pour un rendu braise éclatant
            nouvelle_sat = min(1.0, s * 1.1)
            
            # Conversion inverse vers RGB
            r_new, g_new, b_new = colorsys.hsv_to_rgb(nouvelle_teinte, nouvelle_sat, v)
            nouveaux_pixels.append((int(r_new * 255), int(g_new * 255), int(b_new * 255), a))
        else:
            # On conserve les zones blanches, grises ou de fond intactes
            nouveaux_pixels.append((r, g, b, a))

    img.putdata(nouveaux_pixels)
    img.save(chemin_sortie, "PNG")
    print(f"Fichier généré : {chemin_sortie}")

# Traitement de vos images
images = ["fougeres.png", "logo_google.jpg", "logo_cdf.jpg"]

for img_path in images:
    nom_sortie = img_path.rsplit(".", 1)[0] + "_rouge.png"
    try:
        vert_vers_rouge(img_path, nom_sortie)
    except FileNotFoundError:
        print(f"Fichier introuvable : {img_path}")