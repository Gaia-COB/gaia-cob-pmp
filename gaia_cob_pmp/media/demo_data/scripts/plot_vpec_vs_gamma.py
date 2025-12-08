import matplotlib.pyplot as plt
import numpy as np
import argparse
from typing import Tuple
from pathlib import Path
from numpy.lib.npyio import NpzFile


def load_vpec_gamma_data(source_id: int) -> NpzFile:
    in_path = (
        Path("..")
        / str(source_id) / f"{source_id}_vpec_vs_gamma.npz"
    )
    return np.load(in_path)


def make_figure() -> Tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    return fig, ax


def setup_axes(ax: plt.Axes) -> None:
    ax.set_xlabel("Systemic Velocity (km/s)")
    ax.set_ylabel("Peculiar Velocity (km/s)")


def setup_ticks(ax: plt.Axes) -> None:
    ax.tick_params(
        axis="both", which="major", length=7, width=1.5, direction="in"
    )
    ax.tick_params(
        axis="both", which="minor", length=4, width=1.0, direction="in"
    )
    ax.minorticks_on()


def add_vpec_vs_gamma(ax: plt.Axes, data: NpzFile) -> None:
    x = data["gamma"]
    y_med = data["vpec"]
    y_lo = data["vpec_lo"]
    y_hi = data["vpec_hi"]

    y_min = y_med.min()
    x_min = x[np.argmin(y_med)]

    ax.plot(x, y_med, lw=2, color='k')
    ax.fill_between(x, y_lo, y_hi, color='green', alpha=0.2)

    # This indicates the location of the minimum peculiar velocity
    # With plotly, it will be nice to include some hover info for this point
    ax.plot(x_min, y_min, marker='o', ms=10, mfc='red', mec='k')


def set_axis_limits(ax: plt.Axes, data: NpzFile) -> None:
    x = data["gamma"]
    x_min = x[np.argmin(data["vpec"])]
    y_lo = data["vpec_lo"]
    y_hi = data["vpec_hi"]

    window = (x.max() - x.min()) * 0.25
    x_left = x_min - window
    x_right = x_min + window
    x_idx = np.where((x >= x_left) & (x <= x_right))[0]
    y_hi_window = y_hi[x_idx]

    y_margin = (y_hi.max() - y_lo.min()) * 0.05
    y_top = y_hi_window.max() + y_margin
    y_bottom = y_lo.min() - y_margin
    ax.set_xlim(x_left, x_right)
    ax.set_ylim(y_bottom, y_top)


def _save_figure(fig: plt.Figure, source_id: int) -> None:
    out_path = (
        Path("..")
        / str(source_id) / f"{source_id}_vpec_vs_gamma.pdf"
    )
    fig.savefig(out_path, bbox_inches='tight')


def entry_point(source_id: int) -> None:
    data = load_vpec_gamma_data(source_id)
    fig, ax = make_figure()
    setup_axes(ax)
    setup_ticks(ax)
    add_vpec_vs_gamma(ax, data)
    set_axis_limits(ax, data)
    _save_figure(fig, source_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot peculiar velocity vs systemic velocity."
    )
    parser.add_argument(
        "source_id",
        type=int,
        help="The source ID to plot.",
    )
    args = parser.parse_args()
    entry_point(args.source_id)
