#!/usr/bin/env python3
"""
Supprime uniquement les lignes provoquant :
DecodeError: Expected: LPAREN
dans un fichier .amr, sans rien modifier d'autre.
"""

from penman import load, DecodeError
import io
import logging

logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("penman").setLevel(logging.ERROR)
logging.getLogger("penman.codec").setLevel(logging.ERROR)

input_path = "data/bias_AMR-500.amr"       # <-- ton fichier original
output_path = "data/bias_AMR-500_clean.amr"  # <-- fichier nettoyé

print(f"🧹 Nettoyage du fichier : {input_path}")

# Lecture initiale
with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

iteration = 0
removed_lines = []

while True:
    iteration += 1
    try:
        # On reconstruit un "fichier" à partir des lignes actuelles
        buffer = io.StringIO("".join(lines))
        _ = list(load(buffer))
        print(f"✅ Aucun problème détecté après {iteration} itération(s).")
        break  # tout est bon

    except DecodeError as e:
        msg = str(e)
        if "Expected: LPAREN" not in msg:
            raise e  # autre erreur → on la laisse remonter

        # Extraire le numéro de ligne de l'erreur
        line_num = None
        for part in msg.splitlines():
            if part.strip().startswith("line "):
                try:
                    line_num = int(part.strip().split()[1])
                    break
                except Exception:
                    pass

        if not line_num or line_num > len(lines):
            raise e

        # Supprime la ligne fautive
        print(f"⚠️ Suppression de la ligne {line_num} (DecodeError: Expected: LPAREN)")
        removed_lines.append(line_num)
        del lines[line_num - 1]  # index base 0
        continue  # retente le parsing

# Sauvegarde finale
with open(output_path, "w", encoding="utf-8") as out:
    out.writelines(lines)

print(f"\n✅ Fichier nettoyé enregistré sous : {output_path}")
print(f"🗑️  Lignes supprimées : {len(removed_lines)} -> {removed_lines}")
