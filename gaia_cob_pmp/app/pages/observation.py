from iommi import Header, Page

from app.forms.observation import DatasetForm, ObservationForm


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
    dataset = DatasetForm(
        auto__exclude=["observation", "upload", "arxiv_url", "ads_url", "bibtex"],
        include=lambda user, observation, **_: hasattr(observation, "dataset")
        and (
            observation.dataset.is_valid or user.is_staff
        ),  # Skip this block if there's no dataset uploaded, or if its invalid (unless user is staff)
        instance=lambda observation, **_: observation.dataset,
        editable=False,
    )
