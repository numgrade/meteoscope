"""Build profiling reports for weather CSV data and expose the CLI entry point."""

from __future__ import annotations

import argparse
import json

from meteoscope import cleaning, plot, stats
from meteoscope.reader import lire_csv


def _colonnes_numeriques(lignes: list[dict]) -> list[str]:
    """Return columns containing at least one numeric value.

    Column names are taken from the first row, so ``lignes`` must be non-empty.
    Values are tested with ``isinstance(value, (int, float))``; consequently,
    booleans are considered numeric as well.
    """
    return [
        cle
        for cle in lignes[0]
        if any(isinstance(ligne.get(cle), (int, float)) for ligne in lignes)
    ]


def generer_rapport(lignes: list[dict]) -> dict:
    """Clean the rows and assemble their summary statistics and outliers.

    Missing-value counts are calculated before duplicate removal. The
    remaining values are converted in place before numeric columns are
    analyzed. The row dictionaries may therefore be mutated; callers can also
    reuse their converted values, for example when plotting.

    Args:
        lignes (list[dict]): Rows read from the source CSV.

    Returns:
        A dictionary containing row and column counts, missing-value and
        duplicate counts, per-column statistics, and IQR outliers.
    """
    manquants = cleaning.compter_manquants(lignes)
    lignes_uniques = cleaning.supprimer_doublons(lignes)
    doublons = len(lignes) - len(lignes_uniques)
    cleaning.typer_colonnes(lignes_uniques)
    numeriques = _colonnes_numeriques(lignes_uniques)
    return {
        "nb_lignes": len(lignes_uniques),
        "nb_colonnes": len(lignes_uniques[0]) if lignes_uniques else 0,
        "manquants": manquants,
        "doublons_supprimes": doublons,
        "stats": {c: stats.decrire_colonne(lignes_uniques, c) for c in numeriques},
        "outliers": {c: stats.outliers_iqr(lignes_uniques, c) for c in numeriques},
    }


def main() -> None:
    """Run the command-line workflow for profiling a CSV file.

    Reads the positional CSV path, prints the JSON report, optionally writes
    it to ``--output``, and optionally saves a histogram for ``--plot``.
    """
    parseur = argparse.ArgumentParser(
        prog="meteoscope",
        description="Profile a CSV file of weather observations.",
    )
    parseur.add_argument("csv", help="path to the CSV file to profile")
    parseur.add_argument("--output", help="write the report as JSON to this file")
    parseur.add_argument("--plot", help="plot a histogram of this column (PNG)")
    args = parseur.parse_args()

    lignes = lire_csv(args.csv)
    rapport = generer_rapport(lignes)

    print(json.dumps(rapport, indent=2, ensure_ascii=False))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fichier:
            json.dump(rapport, fichier, indent=2, ensure_ascii=False)

    if args.plot:
        chemin = plot.histogramme(lignes, args.plot, f"histogramme_{args.plot}.png")
        print(f"Chart written: {chemin}")


if __name__ == "__main__":
    main()
