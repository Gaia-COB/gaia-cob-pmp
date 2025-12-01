from typing import Any

from dash_bootstrap_templates import load_figure_template
from django.db.models import Count, QuerySet
from django.template import Template
from iommi import (
    Column,
    Header,
    Page,
    Table,
    html,
)
from pandas import DataFrame
from plotly.graph_objects import Figure, Histogram, Layout
from plotly.graph_objs.layout import XAxis, YAxis
from plotly.offline import plot


class IndexPage(Page):
    """
    Simple index page.
    """

    header = Header("Proposal Management Platform")
    p = html.p("Whatever intro text")


# class RankingPage(Page):
#     """
#     Ranking of bird owners by number of birds
#
#     NOT USED: This is just left in so you can see how to add plotly plots through Iommi extras
#     """
#
#     h1 = html.h1("Most Birds Awards")
#     p = html.p("This award is sponsored by the RSPB")
#
#     table = Table(
#         auto=dict(model=Owner, include=["name", "bird_set"]),
#         columns=dict(
#             name__sortable=False,
#             bird_set=dict(
#                 render_column=False,  # We can still use the data from this column for searches, sorting e.t.c.
#                 # For simple things like this, you can instead do bird_set__render_column=False
#             ),
#             bird_count=Column(
#                 cell__value=lambda row, **_: row.bird_set.count(),
#                 auto_rowspan=True,
#                 sortable=False,
#             ),
#         ),
#         default_sort_order="bird_count",
#     )
#     plotly = Template("{{ page.extra_evaluated.plotly | safe }}")
#
#     class Meta:
#         @staticmethod
#         def extra_evaluated__plotly(params: dict[str, Any], **_) -> str:
#             """
#             Loads data from the database, and renders it into a plot.
#
#             :param params: The page parameters, including the load function it's for.
#             :return: A div containing the rendered plot (or an empty string if no plot is needed).
#             """
#             load_figure_template("bootstrap_dark")
#             queryset: QuerySet[Owner] = Owner.objects.annotate(bird_count=Count("bird_set"))
#             df: DataFrame = DataFrame(list(queryset.values("bird_count")))
#
#             figure: Figure = Figure(
#                 data=[Histogram(x=df["bird_count"])],
#                 layout=Layout(
#                     template="bootstrap_dark",
#                     xaxis=XAxis(title="Number of birds"),
#                     yaxis=YAxis(title="Number of owners"),
#                 ),
#             )
#             return plot(figure, output_type="div")


class PrivacyPage(Page):
    """
    Simple privacy page.
    """

    header = Header("Privacy Notice")
    paragraph = html.p(
        # You can put text here, but the children come before it
        children=dict(
            first=html.p("You probably need a default privacy notice. They're easy to make: "),
            link=html.a(
                "ICO Template here",
                attrs__href="https://ico.org.uk/for-organisations/advice-for-small-organisations/privacy-notices-and-cookies/create-your-own-privacy-notice/privacy-notice-generator-for-customers-or-suppliers/",
            ),
            note=html.p(
                "Realistically, the best way to add this is to put it in a template file and include that."
            ),
        )
    )
    # Add at the top: `from django.template.base import Fragment`
    # template = Fragment(template="path/to/template.html")
