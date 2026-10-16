"""Plots: the ONLY module allowed to use matplotlib."""

from __future__ import annotations

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")  # render without a GUI window (PNG output)


def histogramme(rows: list[dict], column: str, output_path: str) -> str:
    """Plot the histogram of a numeric column and save it as a PNG.

    Returns the path of the generated file.
    """
    values = [row[column] for row in rows if isinstance(row.get(column), (int, float))]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(values, bins=20)
    ax.set_xlabel(column)
    ax.set_ylabel("number of observations")
    ax.set_title(f"Histogram of “{column}”")
    fig.savefig(output_path)
    plt.close(fig)
    return output_path
