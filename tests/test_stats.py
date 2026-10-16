"""Tests of the stats module."""

from __future__ import annotations

import pytest

from meteoscope.stats import decrire_colonne, outliers_iqr


def _lignes(colonne: str, valeurs: list[float]) -> list[dict]:
    """Build rows mapping the given column to each value."""
    return [{colonne: v} for v in valeurs]


def test_decrire_colonne_petit_jeu() -> None:
    """Check descriptive statistics for a small dataset."""
    description = decrire_colonne(_lignes("valeur", [1, 2, 3, 4]), "valeur")
    assert description["nb"] == 4
    assert description["min"] == 1
    assert description["max"] == 4
    assert description["moyenne"] == pytest.approx(2.5)
    assert description["mediane"] == 2.5
    assert description["ecart_type"] == pytest.approx(1.291, rel=1e-2)
    assert description["q1"] == pytest.approx(1.25)
    assert description["q3"] == pytest.approx(3.75)


def test_decrire_colonne_ignore_none() -> None:
    """Check that missing values are excluded from column statistics."""
    lignes = [{"valeur": 1}, {"valeur": None}, {"valeur": 3}]
    description = decrire_colonne(lignes, "valeur")
    assert description["nb"] == 2
    assert description["max"] == 3


def test_outliers_valeur_aberrante() -> None:
    """Check that the IQR method identifies an extreme value as an outlier."""
    lignes = _lignes("valeur", [1, 2, 3, 4, 5, 6, 7, 8, 9, 100])
    assert outliers_iqr(lignes, "valeur") == [100]


def test_outliers_jeu_vide() -> None:
    """Check that outlier detection returns an empty list for empty input."""
    assert outliers_iqr(_lignes("valeur", []), "valeur") == []
