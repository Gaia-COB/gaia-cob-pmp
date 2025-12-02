from iommi import Header, Page

from app.forms.proposal import ProposalForm

class ProposalViewPage(Page):
    """
    The basic view for a project.
    """

    header = Header(lambda proposal, **_: proposal)
    detail = ProposalForm(
        instance=lambda proposal, **_: proposal,
        editable=False,
    )
