"""Descriptive statistics and outlier detection."""

from __future__ import annotations

import statistics


def _valeurs_numeriques(lignes: list[dict], colonne: str) -> list[float]:
    return [ligne[colonne] for ligne in lignes if isinstance(ligne.get(colonne), (int, float))]


def decrire_colonne(lignes: list[dict], colonne: str) -> dict:
    """Descriptive stats of a numeric column (None values ignored)."""
    valeurs = _valeurs_numeriques(lignes, colonne)
    if not valeurs:
        return {"nb": 0}
    q1 = q3 = 0.0
    if len(valeurs) >= 2:
        q1, _, q3 = statistics.quantiles(valeurs, n=4)
    elif len(valeurs) == 1:
        q1 = q3 = valeurs[0]
    return {
        "nb": len(valeurs),
        "min": min(valeurs),
        "max": max(valeurs),
        "moyenne": statistics.mean(valeurs),
        "mediane": statistics.median(valeurs),
        "ecart_type": statistics.stdev(valeurs) if len(valeurs) > 1 else 0.0,
        "q1": q1,
        "q3": q3,
    }


def outliers_iqr(lignes: list[dict], colonne: str) -> list[float]:
    """Values outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR]."""
    valeurs = _valeurs_numeriques(lignes, colonne)
    if len(valeurs) < 4:
        return []
    q1, _, q3 = statistics.quantiles(valeurs, n=4)
    iqr = q3 - q1
    borne_basse, borne_haute = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return [v for v in valeurs if v < borne_basse or v > borne_haute]
