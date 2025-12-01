from iommi import Header, Page

from app.forms.source import SourceForm, SourceGaiaInfoForm


class SourceViewPage(Page):
    """
    The basic view for a source.

    Needs to include all the plots too!
    """

    header = Header(lambda source, **_: source)
    detail = SourceForm(
        auto__exclude=["is_valid"],
        instance=lambda source, **_: source,
        editable=False,
    )
    gaia_info = SourceGaiaInfoForm(
        auto__exclude=["is_active", "source"],
        include=lambda source, **_: hasattr(
            source, "gaiainfo"
        ),  # Skip this block if we don't have Gaia info
        instance=lambda source, **_: source.gaiainfo,
        editable=False,
    )

    # Include plots as well
