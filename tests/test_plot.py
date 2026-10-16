"""Tests for the plot module."""

from __future__ import annotations

from meteoscope.plot import histogramme


def test_histogramme_cree_un_png(tmp_path) -> None:
    """Verify histogramme creates a PNG at the requested path."""
    lignes = [{"temperature_c": v} for v in (1.0, 2.0, 3.0, 4.0, 5.0)]
    chemin = tmp_path / "histogramme.png"
    retour = histogramme(lignes, "temperature_c", str(chemin))
    assert chemin.exists()
    assert retour == str(chemin)
