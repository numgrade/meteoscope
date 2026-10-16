"""Tests for the cleaning module."""

from __future__ import annotations

from meteoscope.cleaning import compter_manquants, supprimer_doublons, typer_colonnes


def test_compter_manquants(donnees_brutes) -> None:
    """Check the count of missing values in each column."""
    manquants = compter_manquants(donnees_brutes)
    # Only columns with at least one None are included:
    assert manquants == {"temperature_c": 1, "humidite_pct": 1}


def test_supprimer_doublons(donnees_brutes) -> None:
    """Check that duplicate rows are removed."""
    uniques = supprimer_doublons(donnees_brutes)
    assert len(uniques) == 3
    assert uniques[0] == donnees_brutes[0]


def test_typer_colonnes(donnees_brutes) -> None:
    """Check column type conversion and preservation of missing values."""
    uniques = supprimer_doublons(donnees_brutes)
    typer_colonnes(uniques)
    premiere = uniques[0]
    assert premiere["temperature_c"] == 3.2
    assert premiere["humidite_pct"] == 87
    assert premiere["station"] == "07149"  # Leading zero is preserved (gotcha).
    assert uniques[1]["temperature_c"] is None
