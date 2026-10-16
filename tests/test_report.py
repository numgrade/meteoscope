"""Tests for the report module."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from meteoscope.report import generer_rapport, main

STATIONS_CSV = Path(__file__).parent.parent / "data" / "stations.csv"


def test_generer_rapport(donnees_brutes) -> None:
    """Check that report generation summarizes the raw data correctly."""
    rapport = generer_rapport(donnees_brutes)
    assert rapport["nb_lignes"] == 3
    assert rapport["doublons_supprimes"] == 1
    assert rapport["manquants"]["temperature_c"] == 1
    assert "temperature_c" in rapport["stats"]
    assert "temperature_c" in rapport["outliers"]


def test_main_ecrit_rapport_json(tmp_path, monkeypatch, capsys) -> None:
    """Check that the command-line entry point writes a JSON report."""
    sortie = tmp_path / "rapport.json"
    monkeypatch.chdir(tmp_path)
    argv = ["meteoscope", str(STATIONS_CSV), "--output", str(sortie)]
    monkeypatch.setattr(sys, "argv", argv)
    main()
    rapport = json.loads(sortie.read_text(encoding="utf-8"))
    assert rapport["nb_lignes"] == 30  # 32 lignes - 2 doublons
    assert rapport["outliers"]["temperature_c"] == [58.3]
    assert "nb_lignes" in capsys.readouterr().out
