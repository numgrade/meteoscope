"""Fixtures partagées entre tous les tests."""

from __future__ import annotations

import pytest


@pytest.fixture
def donnees_brutes() -> list[dict]:
    """Lignes telles que produites par ``reader.lire_csv`` (str ou None).

    Contient volontairement : une valeur manquante, un doublon exact
    (1re et 4e lignes) et une valeur aberrante ("58.3").
    """
    return [
        {"station": "07149", "temperature_c": "3.2", "humidite_pct": "87"},
        {"station": "07149", "temperature_c": None, "humidite_pct": "85"},
        {"station": "07150", "temperature_c": "58.3", "humidite_pct": None},
        {"station": "07149", "temperature_c": "3.2", "humidite_pct": "87"},
    ]
