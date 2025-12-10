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
    p = html.p("Intro text.")


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
