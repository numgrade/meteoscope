"""Helpers for inspecting missing values, removing duplicate rows, and typing data."""

from __future__ import annotations


def compter_manquants(lignes: list[dict]) -> dict[str, int]:
    """Count ``None`` values for each column encountered in the rows.

    Columns with no ``None`` values are omitted. A column absent from a row
    is not counted as missing.
    """
    manquants: dict[str, int] = {}
    for ligne in lignes:
        for cle, valeur in ligne.items():
            if valeur is None:
                manquants[cle] = manquants.get(cle, 0) + 1
    return manquants


def supprimer_doublons(lignes: list[dict]) -> list[dict]:
    """Keep the first row for each repeated sequence of dictionary items.

    Rows are considered duplicates when their ``dict.items()`` tuples match,
    including key order. Values must be hashable. The returned list contains
    the original row dictionaries; they are not copied.
    """
    vues: set[tuple] = set()
    uniques: list[dict] = []
    for ligne in lignes:
        empreinte = tuple(ligne.items())
        if empreinte not in vues:
            vues.add(empreinte)
            uniques.append(ligne)
    return uniques


def typer_colonnes(lignes: list[dict]) -> None:
    """Convert string values in each row in place when possible.

    Values are converted to ``int`` first, then to ``float`` if integer
    conversion fails. Other strings are left unchanged. Strings beginning
    with ``0`` followed by a digit are preserved to avoid losing leading
    zeros (for example, ``"07149"``); strings such as ``"0.0"`` are converted.
    """
    for ligne in lignes:
        for cle, valeur in ligne.items():
            if isinstance(valeur, str):
                ligne[cle] = _convertir(valeur)


def _convertir(valeur: str) -> int | float | str:
    """Convert a numeric string to ``int`` or ``float``, or return it unchanged.

    Preserve strings beginning with ``0`` followed by a digit because
    conversion would discard a potentially significant leading zero.
    """
    if len(valeur) > 1 and valeur[0] == "0" and valeur[1].isdigit():
        return valeur  # "07149": identifier with leading zero, preserve it
    try:
        return int(valeur)
    except ValueError:
        try:
            return float(valeur)
        except ValueError:
            return valeur
