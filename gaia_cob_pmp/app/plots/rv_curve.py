import pandas as pd
import plotly.graph_objects as go
from core.settings import MEDIA_ROOT
from plotly.offline import plot

from app.models import Source

x_margin = 5


def load_gaia_rv_data(source: Source) -> pd.DataFrame:
    try:
        gaia_rv = source.gaiainfo.radial_velocity
        gaia_rv_err = source.gaiainfo.radial_velocity_error

        # Check both values actually exist
        assert gaia_rv is not None
        assert gaia_rv_err is not None

        return gaia_rv, gaia_rv_err

    except (AttributeError, AssertionError):
        raise ValueError("No rv given for source")


def load_rv_data(source: Source) -> pd.DataFrame:
    try:
        source_id = source.gaiainfo.gaia_id
    except AttributeError:
        raise ValueError("No Gaia info for source")
    in_path = f"{MEDIA_ROOT}/demo_data/{source_id}/{source_id}_obs_info_and_rv.csv"
    try:
        data = pd.read_csv(in_path)
        return data
    except FileNotFoundError:
        raise ValueError("No rv file provided for source_id")


def get_rv_plot(source: Source):
    # Get data from hardcoded demo datafiles for now
    data = load_rv_data(source)

    x = data["jd"] - data["jd"].min()
    y = data["rv"]
    yerr = data["rv_err"]

    # Setup figure
    fig = go.Figure()


    # Plot Gaia RV bounds if available
    try:
        gaia_rv, gaia_rv_err = load_gaia_rv_data(source)
        got_gaia_rv = True
    except ValueError:
        got_gaia_rv = False

    if got_gaia_rv:
        x_range = (-x_margin, data["jd"].max() - data["jd"].min() + x_margin)
        y1 = gaia_rv - gaia_rv_err
        y2 = gaia_rv + gaia_rv_err

        # Add hidden trace to enable fillbetween to latch to it
        fig.add_trace(
            go.Scatter(
                x=[-1e32, 1e32],
                y=[y1, y1],
                mode="lines",
                name="Gaia V_rad -error",
                line={"color": "red", "width": 0},
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[-1e32, 1e32],
                y=[y2, y2],
                mode="lines",
                name="Gaia V_rad +error",
                fill="tonexty",
                line={"color": "red", "width": 0},
            )
        )
        fig.add_annotation(
            x=0.5 * (x_range[0] + x_range[1]),
            y=gaia_rv,
            text="Gaia RV ± 1σ",
            xanchor="right",
        )

    # Plot central line
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            error_y=dict(type="data", array=yerr, visible=True),
            name="V_rad",
            marker={
                "symbol": "circle",
                "color": "green",
                "size": 10,
                "line": dict(width=2, color="black"),
            },
        )
    )

    fig.update_xaxes(
        minor=dict(ticklen=4, tickmode="auto", nticks=10, showgrid=True),
        ticklen=7,
        tickmode="auto",
        showgrid=True,
        title=f"Time since JD {data['jd'].min():.1f} (days)",
    )
    fig.update_yaxes(
        minor=dict(ticklen=4, tickmode="auto", nticks=10, showgrid=True),
        ticklen=7,
        tickmode="auto",
        showgrid=True,
        title="Radial Velocity (km/s)",
    )
    fig.update_layout(
        showlegend=False, xaxis_range=[-x_margin, data["jd"].max() - data["jd"].min() + x_margin]
    )

    return plot(fig, output_type="div")
