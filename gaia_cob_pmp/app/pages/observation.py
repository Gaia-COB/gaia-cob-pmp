from iommi import Header, Page
from iommi._web_compat import Template

from app.forms.observation import DatasetForm, ObservationForm
from app.plots.spectrum import get_spectrum_plot


class ObservationViewPage(Page):
    """
    The basic view for an observation.
    """

    header = Header(
        lambda observation,
        **_: f"{observation.proposal.instrument} observation of {observation.source}"
    )
    detail = ObservationForm(
        auto__exclude=["is_valid"],
        instance=lambda observation, **_: observation,
        editable=False,
    )
    data_plot = Template("{{ page.extra_evaluated.data_plot | safe }}")
    dataset = DatasetForm(
        auto__exclude=[
            "observation",
            "upload",
            "arxiv_url",
            "ads_url",
            "bibtex",
            "flux_col",
            "flux_err_col",
            "flux_units",
            "wavelength_col",
            "wavelength_units",
            "is_valid",
        ],
        include=lambda user, observation, **_: hasattr(observation, "dataset")
        and (
            observation.dataset.is_valid or user.is_staff
        ),  # Skip this block if there's no dataset uploaded, or if its invalid (unless user is staff)
        instance=lambda observation, **_: observation.dataset,
        editable=False,
    )

    class Meta:
        @staticmethod
        def extra_evaluated__data_plot(observation, **_) -> str:
            """
            Generates and renders the plot for a given spectrum dataset if relevant data is present
            """
            try:
                # Get the vpec_vs_gamma plot
                figure = get_spectrum_plot(observation)
                return figure
            except AssertionError:
                # If plot could not be generated (if source has no DataSet or there's no file to draw from), skip and return an empty fragment
                return ""
