import matplotlib.pyplot as plt
import pandas as pd
import argparse
from typing import Tuple
from pathlib import Path


df_source_info = pd.read_csv(
    "../source_gaia_info.csv"
)

x_margin = 5


def load_rv_data(source_id: int) -> pd.DataFrame:
    in_path = (
        Path("../../../data/example_spectral_data")
        / str(source_id) / f"{source_id}_obs_info_and_rv.csv"
    )
    return pd.read_csv(in_path)


def make_figure() -> Tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))

    return fig, ax


def setup_axes(ax: plt.Axes, data: pd.DataFrame) -> None:
    first_jd = data["jd"].min()
    ax.set_xlabel(f"Time since JD {first_jd:.1f} (days)")
    ax.set_ylabel("Radial Velocity (km/s)")


def setup_ticks(ax: plt.Axes) -> None:
    ax.tick_params(
        axis="both", which="major", length=7, width=1.5, direction="in"
    )
    ax.tick_params(
        axis="both", which="minor", length=4, width=1.0, direction="in"
    )
    ax.minorticks_on()


def add_rv_data(ax: plt.Axes, data: pd.DataFrame) -> None:
    x = data["jd"] - data["jd"].min()  # Time in days since the first epoch
    y = data["rv"]
    yerr = data["rv_err"]

    ax.errorbar(
        x, y, yerr=yerr, marker='o', ms=7, mfc='green', mec='k', ecolor='k',
        elinewidth=1.0, capsize=4, ls='none'
    )


def add_gaia_rv(ax: plt.Axes, source_id: int, data: pd.DataFrame) -> None:
    row = df_source_info[df_source_info["source_id"] == source_id]
    gaia_rv = row["radial_velocity"].values[0]
    gaia_rv_err = row["radial_velocity_error"].values[0]
    x_range = (-x_margin, data["jd"].max() - data["jd"].min() + x_margin)
    ax.fill_between(
        x=x_range,
        y1=gaia_rv - gaia_rv_err,
        y2=gaia_rv + gaia_rv_err,
        color='r',
        alpha=0.2
    )

    ax.text(
        0.5 * (x_range[0] + x_range[1]), gaia_rv, 'Gaia RV ± 1σ',
        color='k', ha='center', va='center'
    )


def setup_ax_lims(ax: plt.Axes, data: pd.DataFrame) -> None:
    ax.set_xlim(-x_margin, data["jd"].max() - data["jd"].min() + x_margin)


def _save_figure(fig: plt.Figure, source_id: int) -> None:
    out_path = (
        Path("../") / str(source_id) / f"{source_id}_rv_curve.pdf"
    )
    fig.savefig(out_path, bbox_inches="tight")


def entry_point(source_id: int) -> None:
    rv_data = load_rv_data(source_id)
    fig, ax = make_figure()
    setup_axes(ax, rv_data)
    setup_ticks(ax)
    add_rv_data(ax, rv_data)
    add_gaia_rv(ax, source_id, rv_data)
    setup_ax_lims(ax, rv_data)
    _save_figure(fig, source_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot radial velocity vs time from a CSV file."
    )
    parser.add_argument(
        "source_id", type=int, help="Source ID for the input data."
    )

    args = parser.parse_args()
    entry_point(args.source_id)
