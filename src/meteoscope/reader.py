"""Read CSV files containing meteorological observations."""

from __future__ import annotations

import csv


def lire_csv(chemin: str, sentinelle: float = -999.9) -> list[dict]:
    """Read meteorological observations from a UTF-8 CSV file.

    Each data row is returned as a dictionary keyed by its column headers.
    Empty cells and values numerically equal to ``sentinelle`` become
    ``None``; other values remain strings. Extra fields in oversized rows
    are ignored. The file is expected to have a header row.

    Args:
        chemin (str): Path to the CSV file.
        sentinelle (float): Numeric missing-value marker to replace with ``None``.

    Returns:
        A list of row dictionaries, in file order.
    """
    with open(chemin, encoding="utf-8", newline="") as fichier:
        lignes_brutes = list(csv.DictReader(fichier))

    lignes: list[dict] = []
    for ligne in lignes_brutes:
        ligne_propre: dict = {}
        for cle, valeur in ligne.items():
            if cle is None:  # extra column in an oversized row
                continue
            if valeur == "" or _est_sentinelle(valeur, sentinelle):
                ligne_propre[cle] = None
            else:
                ligne_propre[cle] = valeur
        lignes.append(ligne_propre)
    return lignes


def _est_sentinelle(valeur: str, sentinelle: float) -> bool:
    """Return whether ``valeur`` parses to the configured sentinel number."""
    try:
        return float(valeur) == sentinelle
    except ValueError:
        return False


def colonnes(entetes: list[str]) -> list[str]:
    """Return a copy of the column headers, preserving their order."""
    return list(entetes)
