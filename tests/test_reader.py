"""Tests of the reader module."""

from __future__ import annotations

from pathlib import Path

import pytest

from meteoscope.reader import colonnes, lire_csv

MINI_CSV = Path(__file__).parent / "data" / "mini.csv"


def test_cellules_vides_deviennent_none(tmp_path) -> None:
    """Verify that empty CSV cells are converted to None."""
    chemin = tmp_path / "mini.csv"
    chemin.write_text("a,b\n1,\n,x\n", encoding="utf-8")
    lignes = lire_csv(str(chemin))
    assert lignes[0]["b"] is None
    assert lignes[1]["a"] is None


def test_sentinelle_devient_none() -> None:
    """Verify that empty cells and sentinel values are converted to None."""
    lignes = lire_csv(str(MINI_CSV))
    assert lignes[0]["temperature_c"] == "3.2"
    assert lignes[1]["temperature_c"] is None  # cellule vide
    assert lignes[2]["temperature_c"] is None  # sentinelle -999.9


def test_nombre_de_lignes_de_mini_csv() -> None:
    """Verify the number of data rows in the mini CSV file."""
    assert len(lire_csv(str(MINI_CSV))) == 4


def test_fichier_inexistant() -> None:
    """Verify that reading a missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        lire_csv("fichier_inexistant.csv")


def test_colonnes() -> None:
    """Verify that colonnes returns the provided column names."""
    assert colonnes(["a", "b", "c"]) == ["a", "b", "c"]
