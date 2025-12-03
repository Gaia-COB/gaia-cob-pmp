from iommi import Header, Page

from app.forms.observation import DatasetForm, ObservationForm


class ObservationViewPage(Page):
    """
    The basic view for a project.
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
    dataset = DatasetForm(
        auto__exclude=["observation", "upload"],
        include=lambda observation, **_: hasattr(
            observation, "dataset"
        ),  # Skip this block if there's no dataset uploaded
        instance=lambda observation, **_: observation.dataset,
        editable=False,
    )
