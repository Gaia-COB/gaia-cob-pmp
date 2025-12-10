from iommi import Header, Page
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
    detail = SourceForm(
        auto__exclude=["is_valid", "name"],
        instance=lambda source, **_: source,
        editable=False,
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
