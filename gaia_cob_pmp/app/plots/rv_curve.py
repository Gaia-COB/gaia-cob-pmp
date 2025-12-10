import pandas as pd
import plotly.graph_objects as go
from django.db.models import F
from plotly.offline import plot

from app.models import DataSet, Observation, Source

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
    qset = DataSet.objects.filter(observation__source=source)
    qset = qset.annotate(jd=F("observation__jd"))

    df = pd.DataFrame(list(qset.values()))

    if df.empty:
        raise ValueError("No valid vr readings")

    return df


def get_rv_plot(source: Source):
    data = load_rv_data(source)

    x = data["jd"] - data["jd"].min()
    y = data["radial_velocity"]
    yerr = data["radial_velocity_error"]

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

    # Plot central line
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            error_y=dict(type="data", array=yerr, visible=True),
            name="V_rad",
            mode="markers",
            marker={
                "symbol": "circle",
                "color": "green",
                "size": 10,
                "line": dict(width=2, color="black"),
            },
        )
    )

    plotAnnotes = []

    # A nasty and a bit hacky way to get hyperlinks onto the plot without needing Dash magic
    # MAY NOT SCALE FOR VERY LARGE DATASETS due to multiple queries!!
    for index, row in data.iterrows():
        obs_obj = Observation.objects.get(pk=row["observation_id"])
        url = obs_obj.get_absolute_url()

        plotAnnotes.append(
            dict(
                x=row["jd"] - data["jd"].min(),
                y=row["radial_velocity"],
                text=f"<a href='{url}'>    </a>",
                showarrow=False,
                xanchor="center",
                yanchor="middle",
            )
        )

    # Add label to Gaia RV range if it was plotted earlier
    if got_gaia_rv:
        plotAnnotes.append(
            dict(
                x=0.5 * (x_range[0] + x_range[1]),
                y=gaia_rv,
                text="Gaia RV ± 1σ",
                xanchor="right",
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
        annotations=plotAnnotes,
        showlegend=False,
        xaxis_range=[-x_margin, data["jd"].max() - data["jd"].min() + x_margin],
    )

    return plot(fig, output_type="div")
