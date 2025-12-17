from django.conf import settings
from django.utils.safestring import mark_safe
from iommi import Asset, Header, Page, html
from iommi._web_compat import Template

from app.forms.source import SourceForm, SourceGaiaInfoForm
from app.plots.rv_curve import get_rv_plot
from app.plots.vpec_vs_gamma import get_vvg_plot


class SourceViewPage(Page):
    """
    The basic view for a source.

    Needs to include all the plots too!
    """

    header = Header(lambda source, **_: source)

    # This could be done using a Panel, but this is simplest
    detail = html.div(
        attrs__class={"row": True},
        children=dict(
            form=SourceForm(
                auto__exclude=["is_valid", "name"],
                instance=lambda source, **_: source,
                editable=False,
                attrs__class={"col-md-9": True},
            ),
            aladin=html.div(
                attrs__id="aladin-lite-div",
                attrs__class={"col-md-3": True},  # Can't have a dict key called 'class'
                assets=dict(
                    aladin_target=Asset.js(
                        lambda source, **_: mark_safe(
                            f'let aladin_target = "{source.get_aladin_coordinates()}";'
                            f'let aladin_fov = {settings.ALADIN_DEFAULT_FOV:.1f};'
                            f'let aladin_survey = {settings.ALADIN_DEFAULT_SURVEY};'
                        )
                    ),
                    aladin_library=Asset.js(attrs__src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js"),
                    aladin=Asset.js(attrs__src="/static/js/source_aladin.js", in_body=True),  # The code that finds the div and renders it
                )
            ),
        )
    )
    vvg_plot = Template("{{ page.extra_evaluated.vvg_plot | safe }}")
    rv_plot = Template("{{ page.extra_evaluated.rv_plot | safe }}")
    gaia_info = SourceGaiaInfoForm(
        auto__exclude=["is_valid", "source"],
        include=lambda source, **_: hasattr(
            source, "gaiainfo"
        ),  # Skip this block if we don't have Gaia info
        instance=lambda source, **_: source.gaiainfo,
        editable=False,
    )

    class Meta:
        @staticmethod
        def extra_evaluated__vvg_plot(source, **_) -> str:
            """
            Generates and renders the vpec_vs_gamma plot for a given source if relevant data is present
            """
            try:
                # Get the vpec_vs_gamma plot
                figure = get_vvg_plot(source)
                return figure
            except ValueError:
                # If plot could not be generated (if source has no Gaiainfo or there's no file to draw from), skip and return an empty fragment
                return ""

        @staticmethod
        def extra_evaluated__rv_plot(source, **_) -> str:
            """
            Generates and renders the rv_curve plot for a given source if relevant data is present
            """
            try:
                # Get the vpec_vs_gamma plot
                figure = get_rv_plot(source)
                return figure
            except ValueError:
                # If plot could not be generated (if source has no Gaiainfo or there's no file to draw from), skip and return an empty fragment
                return ""
