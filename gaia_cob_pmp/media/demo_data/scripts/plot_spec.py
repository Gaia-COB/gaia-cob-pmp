import matplotlib.pyplot as plt
import pandas as pd
import argparse
from typing import Tuple
from pathlib import Path


def load_spectrum(in_path: Path) -> pd.DataFrame:
    return pd.read_csv(in_path)


def make_figure() -> Tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))

    return fig, ax


def setup_axes(ax: plt.Axes) -> None:
    ax.set_xlabel("Wavelength (Angstrom)")
    ax.set_ylabel("Flux (arbitrary units)")


def setup_ticks(ax: plt.Axes) -> None:
    ax.tick_params(
        axis="both", which="major", length=7, width=1.5, direction="in"
    )
    ax.tick_params(
        axis="both", which="minor", length=4, width=1.0, direction="in"
    )
    ax.minorticks_on()


def add_spectrum(ax: plt.Axes, data: pd.DataFrame) -> None:
    wave = data["wavelength"]
    flux = data["flux"]
    ax.plot(wave, flux, lw=1.0, color="k")


def _save_figure(fig: plt.Figure, out_path: Path) -> None:
    fig.savefig(out_path, bbox_inches="tight")


def entry_point(in_path: Path, out_path: Path) -> None:
    fig, ax = make_figure()
    setup_axes(ax)
    setup_ticks(ax)
    spec = load_spectrum(in_path)
    add_spectrum(ax, spec)
    _save_figure(fig, out_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot a spectrum from a CSV file."
    )
    parser.add_argument(
        "in_path", type=Path, help="Path to input CSV file."
    )
    parser.add_argument(
        "out_path", type=Path, help="Path to output image file."
    )

    args = parser.parse_args()

    entry_point(args.in_path, args.out_path)
